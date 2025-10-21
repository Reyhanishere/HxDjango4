from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
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
            TextBlock, ImageBlock, MCQBlock, KeyFeatureBlock, PairingBlock, MonoTextCheckBlock,
        ).filter(
            Q(textblock__visible=True) |
            Q(imageblock__visible=True) |
            Q(mcqblock__visible=True) |
            Q(keyfeatureblock__visible=True) |
            Q(pairingblock__visible=True) |
            Q(monotextcheckblock__visible=True)
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
            TextBlock, ImageBlock, MCQBlock, KeyFeatureBlock, PairingBlock, MonoTextCheckBlock
        ).filter(
            Q(textblock__visible=True) |
            Q(imageblock__visible=True) |
            Q(mcqblock__visible=True) |
            Q(keyfeatureblock__visible=True) |
            Q(pairingblock__visible=True) |
            Q(monotextcheckblock__visible=True)
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
            current_block = blocks.filter(number=1).first()

        # context['blocks'] = blocks  # still available if needed
        context['current_block'] = current_block
        return context
    
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
                a = f"dot.node('B{b.number}', shape='box', style='rounded', label='{b.question_text.replace(b_n, space)[:50]}')<br/>"
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

def submit_course_race_score(request, uuid, race_id):
    race = get_object_or_404(Race, id=race_id)

    # if the race is linked to any course → require login
    # if race.course.exists() and not request.user.is_authenticated:
    #     messages.error(request, "You must log in to participate in course races.")
    #     return redirect('login')

    # if request.user.is_authenticated and Record.objects.filter(race=race, user=request.user).exists():
    #     messages.error(request, "You have already submitted this race.")
    #     return redirect('race_detail', race_id=race.id)
    course = Course.objects.get(id=uuid)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        

        try:
            score = int(score)
        except (TypeError, ValueError):
            score = 0

        record, created = Record.objects.get_or_create(user=request.user, course=course, race=race, defaults={
            'score': score,
        })

        if created:
            record.save()

            messages.success(request, f"Your score: {score}")
            return redirect('course_detail', uuid=uuid)
        else: 
            messages.error(request, f"You have already done the test.")
            return redirect('course_detail', uuid=uuid)


from django.db.models import Sum

@login_required
def course_detail(request, uuid):
    course = get_object_or_404(Course, id=uuid)

    # professor view
    if request.user == course.professor:
        students = course.students.all()

        # total score per student
        total_scores = (
            Record.objects.filter(course=course)
            .values('user__id', 'user__username')
            .annotate(total_score=Sum('score'))
        )

        # per-race scores
        # race_scores = (
        #     Record.objects.filter(course=course)
        #     .values('race__name', 'user__username', 'score')
        #     .order_by('race__name')
        # )
        races_scores = []
        for race in course.races.all():
            temp = []
            recs = Record.objects.filter(course=course, race=race).order_by('-score')
            for r in recs:
                temp.append({'name': r.user.get_name(), 'score': r.score,})
            races_scores.append({'race_name': race.name, 'data':temp, 'id':race.id})
        regs = CourseRegistration.objects.filter(course=course)
        students_list = []
        for r in regs:
            students_list.append(r.student.get_name())
        return render(request, 'steps/course_professor.html', {
            'course': course,
            'students': students,
            'total_scores': total_scores,
            'races_scores': races_scores,
            'students_list':students_list,
        })
        return render(request, 'steps/course_professor.html', {
            'course': course,
            'students': students,
            'total_scores': total_scores,
            'races_scores': races_scores,
        })

    # student view
    elif request.user in course.students.all():
        races = course.races.all()
        records = Record.objects.filter(course=course, user=request.user)
        record_dict = {r.race_id: r.score for r in records}
        races_data=[]
        for race in races:
            try:
                Step.objects.get(race=race)
                record=Record.objects.filter(course=course, user=request.user, race=race).last()
                if record:
                    races_data.append({'name': race.name, 'score': record.score,})
                else:
                    races_data.append({'name': race.name, 'score': None, 'id':race.id})
            except:
                pass
        print(races_data)

        return render(request, 'steps/course_student.html', {
            'course': course,
            'races': races,
            'races_data': races_data,
        })

    # outsider view
    else:
        return render(request, 'steps/course_register.html', {'course': course})

@login_required
def register_course(request, uuid):
    course = get_object_or_404(Course, id=uuid)
    course.students.add(request.user)
    messages.success(request, "You have successfully registered in this course.")
    return redirect('course_detail', uuid=course.id)

@login_required
def course_race_view(request, uuid, race_id):
    course = get_object_or_404(Course, id=uuid)
    race = get_object_or_404(Race, id=race_id, course=course)

    # Prevent duplicate submission
    if Record.objects.filter(course=course, race=race, user=request.user).exists():
        messages.error(request, "You have already submitted this race.")
        return redirect('course_detail', uuid=course.id)

    if request.method == 'POST':
        score = request.POST.get('score')
        Record.objects.create(
            race=race,
            course=course,
            user=request.user,
            score=score
        )
        messages.success(request, f"Your score: {score}")
        return redirect('course_detail', uuid=course.id)

    return render(request, 'steps/ranking.html', {'race': race, 'course': course})

class StepCourseRaceDetailView(LoginRequiredMixin, DetailView):
    model = Step
    template_name = 'steps/step_course_race_detail.html'
    context_object_name = 'step'

    def get_object(self):
        # get race by id from URL
        race_id = self.kwargs.get('race_id')
        race = Race.objects.get(id=race_id)

        try:
            return Step.objects.get(race=race)
        except Step.DoesNotExist:
            raise Http404("Race not found")

    def dispatch(self, request, *args, **kwargs):
        course_uuid = kwargs.get('uuid')
        course = get_object_or_404(Course, id=course_uuid)

        # only allow students or professor to access
        user = request.user
        if not (course.students.filter(id=user.id).exists() or user == course.professor):
            return redirect('course_register', uuid=course.uuid)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        step = self.object
        
        if not step.race:
            raise Http404("This step is not a race")

        visible_blocks = step.blocks.instance_of(
            TextBlock, ImageBlock, MCQBlock, KeyFeatureBlock, PairingBlock, MonoTextCheckBlock
        ).filter(
            Q(textblock__visible=True) |
            Q(imageblock__visible=True) |
            Q(mcqblock__visible=True) |
            Q(keyfeatureblock__visible=True) |
            Q(pairingblock__visible=True) |
            Q(monotextcheckblock__visible=True)
        )

        context['blocks'] = visible_blocks
        context['course'] = get_object_or_404(Course, id=self.kwargs.get('uuid'))

        return context




