from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import *


class StepListView(ListView):
    model = Step
    template_name = 'steps/step_list.html'

class StepDetailView(DetailView):
    model = Step
    template_name = 'steps/step_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object
        
        # Get all specific block types you have
        visible_blocks = step.blocks.instance_of(
            TextBlock, ImageBlock, MCQBlock, KeyFeatureBlock, PairingBlock
        ).filter(
            Q(textblock__visible=True) |
            Q(imageblock__visible=True) |
            Q(mcqblock__visible=True) |
            Q(keyfeatureblock__visible=True) |
            Q(pairingblock__visible=True)
        )
        
        context['blocks'] = visible_blocks
        return context
        
class StepRaceDetailView(DetailView):
    model = Step
    template_name = 'steps/step_race_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object
        if not step.race:
            from django.http import Http404
            raise Http404
        
        # Get all specific block types you have
        visible_blocks = step.blocks.instance_of(
            TextBlock, ImageBlock, MCQBlock, KeyFeatureBlock, PairingBlock
        ).filter(
            Q(textblock__visible=True) |
            Q(imageblock__visible=True) |
            Q(mcqblock__visible=True) |
            Q(keyfeatureblock__visible=True) |
            Q(pairingblock__visible=True)
        )
        
        context['blocks'] = visible_blocks
        return context
        
class InteractiveStepDetailView(DetailView):
    model = InteractiveStep
    template_name = 'steps/interactive_step_detail.html'
    context_object_name = 'step'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object

        blocks = step.interactive_blocks.instance_of(
            InteractiveImageBlock,
            InteractiveTextBlock,
            InteractiveQuestionBlock
        )

        # Handle dynamic block loading based on URL query param
        block_number = self.request.GET.get('block')
        if block_number:
            current_block = blocks.filter(number=block_number).first()
        else:
            current_block = blocks.first()

        # context['blocks'] = blocks  # still available if needed
        context['current_block'] = current_block
        return context
    
def load_interactive_block(request, step_id, block_number):
    step = get_object_or_404(InteractiveStep, id=step_id)
    blocks = step.interactive_blocks.instance_of(
        InteractiveImageBlock,
        InteractiveTextBlock,
        InteractiveQuestionBlock
    )
    block = blocks.filter(number=block_number).first()
    if not block:
        return render(request, 'steps/_end_of_step.html')

    return render(request, 'steps/_interactive_blocks.html', {'block': block})

class InteractiveStepGraphVizz(DetailView):
    model = InteractiveStep
    template_name = 'steps/interactive_step_graph.html'
    context_object_name = 'step'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object

        blocks = step.interactive_blocks.instance_of(
            InteractiveImageBlock,
            InteractiveTextBlock,
            InteractiveQuestionBlock
        )
        COLORS={'red':'#f8d7da', 'yellow':'#fff3cd', 'blue':'#cce5ff', 'green':'#d4edda'}
        o_n = 0
        final_text = ""
        b_n='\n'
        space = ' '
        for b in blocks:
            if b.__class__.__name__=='InteractiveQuestionBlock':
                a = f"dot.node('B{b.number}', shape='box', style='solid', label='{b.question_text.replace(b_n, space)[:50]}')<br/>"
                final_text+=a
                options = b.options.all()
                a="dot.attr('node', shape='ellipse', style='filled')<br/>"
                final_text+=a
                for o in options:
                    if o.__class__.__name__=='InteractiveTextOption':
                        a=f"dot.node('O{o_n}', color='{COLORS[o.color]}', label='{o.text.replace(b_n, space)}')<br/>"
                        a+=f"dot.edge('B{b.number}', 'O{o_n}')<br/>"
                        if o.next_block_number:
                            a+=f"dot.edge('O{o_n}', 'B{o.next_block_number}')<br/>"
                        final_text+=a
                    o_n+=1
            elif b.__class__.__name__=='InteractiveImageBlock':
                a = f"dot.node('B{b.number}', shape='box', style='solid', label='{b.caption.replace(b_n, space)[:50]}')<br/>"
                if b.next_block_number:
                    a+=f"dot.edge('B{b.number}', 'B{b.next_block_number}')<br/>"
                final_text+=a
            else:
                txt_content = " ".join(b.content.split())
                a = f"dot.node('B{b.number}', shape='box', style='solid', label='{txt_content[:50]}')<br/>"
                if b.next_block_number:
                    a+=f"dot.edge('B{b.number}', 'B{b.next_block_number}')<br/>"
                final_text+=a
        context['ehsan'] = final_text
        return context

        
def submit_answer(request, block_id):
    if request.method == 'POST':
        block = get_object_or_404(Block, pk=block_id)
        data = request.POST.get('data')
        # Process and evaluate the answer
        UserAnswer.objects.create(
            user=request.user if request.user.is_authenticated else None,
            block=block,
            submitted_data=data,
            is_correct=False  # Temporary; evaluation logic comes here
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def ranking_page(request, race_id):
    race = Race.objects.get(id=race_id)
    records = race.records.order_by('-score', 'timestamp')[:100]
    return render(request, 'steps/ranking.html', {'records': records, 'race': race})

def get_client_ip(request):
    """Handles IP even behind proxy/load balancer"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def submit_race_score(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        score = request.POST.get('score')
        ip = get_client_ip(request)

        # Convert score to int safely
        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        if Record.objects.filter(race=race, ip_address=ip).exists():
            return JsonResponse({
                "status": 400,
                "message": f"⚠️ You have already submitted. <span style='font-size: 12px'>Duplicate IP</span>"
             })
        if Record.objects.filter(race=race, name=name).exists():   
            return JsonResponse({
                "status": 400,
                "message": f"⚠️ Choose another nickname. <b>{name}</b> is already taken."
             })


        Record.objects.create(race=race, name=name, score=score, ip_address=ip)
        return JsonResponse({
            "status": "ok",
            "redirect_url": reverse('ranking_page', args=[race.id])
        })

    return JsonResponse({
            "status": 400,
            "redirect_url": "❌ Invalid request."
        })





