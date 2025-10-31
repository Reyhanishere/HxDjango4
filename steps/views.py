from django.urls import reverse
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

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

def my_rank(request, race_id, id_score):
    record_id, score = str(id_score).split("_")
    record_id, score = int(record_id), int(score)
    race = get_object_or_404(Race, id=race_id)
    record = get_object_or_404(Record, id=record_id, race=race)

    # Check if the user has already submitted a survey for this race
    existing_survey = SurveyRecord.objects.filter(
        race=race, author=record.name
    ).first()

    try:
        highest_score_object = Record.objects.filter(race=race).order_by('score').last()
        highest_score = highest_score_object.score
    except:
        highest_score = None

    score_matches = record.score == score

    context = {
        'race': race,
        'record': record,
        'score_matches': score_matches,
        'highest_score': highest_score,
        'num_list': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
    }

    if score_matches:
        ranking = record.get_ranking()
        total_records = Record.objects.filter(race=race).count()
        same_score_records = Record.objects.filter(race=race, score=score).count()

        context.update({
            'ranking': ranking,
            'total_records': total_records,
            'same_score_records': same_score_records,
        })

    # If survey already exists → show thank you / summary instead of form
    if existing_survey:
        context['existing_survey'] = existing_survey
        return render(request, 'steps/my_record.html', context)

    # Otherwise → handle new survey submission
    if request.method == 'POST':
        survey_score = int(request.POST.get('survey_score'))
        text_box = request.POST.get('text_box')

        SurveyRecord.objects.create(
            author=record.name,
            race_score=record.score,
            survey_score=survey_score,
            race=race,
            text_box=text_box,
        )
        return redirect('my_rank', race_id=race.id, id_score=id_score)

    return render(request, 'steps/my_record.html', context)

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

        if not race.is_open():
            return JsonResponse({
                "status": 400,
                "message": f"⚠️ Time to participate at this race has ended."
             })

        else:
            if Record.objects.filter(race=race, ip_address=ip).exists():
                return JsonResponse({
                    "status": 400,
                    "message": f"⚠️ You have already submitted. <span style='font-size: 12px'>Duplicate IP</span>"
                })
            elif Record.objects.filter(race=race, name=name).exists():   
                return JsonResponse({
                    "status": 400,
                    "message": f"⚠️ Choose another nickname. <b>{name}</b> is already taken."
                })
            else:
                record = Record(race=race, name=name, score=score, ip_address=ip)
                record.save()
                # Record.objects.create(race=race, name=name, score=score, ip_address=ip)
                return JsonResponse({
                    "status": "ok",
                    "redirect_url": reverse('my_rank', args=[race_id ,f"{record.id}_{score}"])
                })

    return JsonResponse({
            "status": 400,
            "redirect_url": "❌ Invalid request."
        })

def submit_course_race_score(request, uuid, race_id):
    race = get_object_or_404(Race, id=race_id)

    # if the race is linked to any course → require login
    if race.course.exists() and not request.user.is_authenticated:
        messages.error(request, "You must log in to participate in course races.")
        return JsonResponse({
                "status": 400,
                "message": f"⚠️ You must log in to participate in course races. It's almost imposible that someone sees this message."
             })

    course = Course.objects.get(id=uuid)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        
        if not course in race.course.all():
            messages.error(request, f"This race is not in the course! Bad link.")
            return JsonResponse({
                "status": 400,
                "message": f"⚠️ This race is not in the course! Where did you get the link from?"
             })
        
        if not course.open_for_answering:
            messages.error(request, f"Course races are not open for score submition.")
            return JsonResponse({
                "status": 400,
                "message": f"⚠️ فرصت ثبت امتیازها در این دوره تمام شده‌است."
             })
        
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
            
            return JsonResponse({
                "status": "ok",
                "redirect_url": reverse('course_detail', args=[uuid]),
             })
            
        else:
            if course.score_correction:
                if score > record.score:
                    record.score = score
                    record.save()
                    return JsonResponse({
                        "status": "ok",
                        "redirect_url": reverse('course_detail', args=[uuid]),
                    })
                else:
                    return JsonResponse({
                        "status": 400,
                        "message": f"⚠️ امتیاز پیشین شما،کمتر نبوده است."
                    })
            else:
                messages.error(request, f"You have already done the test.")
                return JsonResponse({
                    "status": 400,
                    "message": f"⚠️ شما پیش‌تر به این پرسش‌ها پاسخ داده‌اید. امکان اصلاح نمره وجود ندارد."
                })


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
            .values('user__id', 'name')
            .annotate(total_score=Sum('score'))
        )
        total_scores_ordered = sorted(total_scores, key=lambda x: x['total_score'], reverse=True)

        races_scores = []
        for race in course.races.all():
            temp = []
            recs = Record.objects.filter(course=course, race=race).order_by('-score')
            for r in recs:
                temp.append({'name': r.user.get_name(), 'score': r.score,})
            races_scores.append({'race_name': race.name, 'data':temp, 'id':race.id})
        regs = CourseRegistration.objects.filter(course=course).order_by('joined_at')
        students_list = []
        for r in regs:
            students_list.append(r.student.get_name())
        return render(request, 'steps/course_professor.html', {
            'course': course,
            'students': students,
            'total_scores': total_scores_ordered,
            'races_scores': races_scores,
            'students_list':students_list,
        })

    # student view
    elif request.user in course.students.all():
        total_score = (
            Record.objects.filter(course=course, user=request.user)
            .values('name')
            .annotate(total_score=Sum('score'))
        )
        total_score = total_score[0]['total_score']
        races = course.races.all()
        races_data=[]
        for race in races:
            try:
                record=Record.objects.filter(course=course, user=request.user, race=race).last()
                if record:
                    races_data.append({'name': race.name, 'score': record.score,})
                else:
                    races_data.append({'name': race.name, 'score': None, 'id':race.id})
            except:
                pass
        
        ## Two Things to do:
        ### 1. Show user's ranking among friends (two aboves and two belows)
        ### 2. If course is closed (need to be added in models) (reg_closed, visible, answer_closed), show their lesson (step) link. Done

        return render(request, 'steps/course_student.html', {
            'course': course,
            'total_score': total_score,
            'races_data': races_data,
        })

    # outsider view
    else:
        lessons = []
        for race in course.races.all():
            lessons.append({'lesson_title':race.step_set.first().title, 
                            'race_name':race.name,
                            'slug':race.step_set.first().slug,
                            'field':race.step_set.first().field})
        return render(request, 'steps/course_register.html', {'course': course, 'lessons':lessons})

@login_required
def course_register(request, uuid):
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
            return redirect('course_register', uuid=course.id)

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

def is_course_professor(user, course):
    return user == course.professor

@login_required
@require_POST
def toggle_course_field(request, course_uuid, field_name):
    course = get_object_or_404(Course, id=course_uuid)
    
    # Check if user is the course professor
    if not is_course_professor(request.user, course):
        messages.error(request, "You don't have permission to modify this course.")
        return redirect(reverse('course_detail', args=[course_uuid]))

    
    valid_fields = ['open_for_registration', 'visible_when_closed', 'open_for_answering', 'score_correction']
    if field_name not in valid_fields:
        messages.error(request, "Invalid field")
        return redirect(reverse('course_detail', args=[course_uuid]))
    
    current_value = getattr(course, field_name)
    setattr(course, field_name, not current_value)
    course.save()
    
    field_display_names = {
        'open_for_registration':'Open for new students registration',
        'visible_when_closed': 'Visible lessons when registration closed',
        'open_for_answering': 'Open for answering', 
        'score_correction': 'Score correction'
    }
    
    messages.success(request, 
        f"{field_display_names[field_name]} {'enabled' if not current_value else 'disabled'}")
    
    return redirect(reverse('course_detail', args=[course_uuid]))

@login_required
@require_POST
def toggle_course_field_post(request, course_uuid, field_name):
    course = get_object_or_404(Course, id=course_uuid)
    
    # Check if user is the course professor
    if not is_course_professor(request.user, course):
        messages.error(request, "You don't have permission to modify this course.")
        return redirect(reverse('course_list'))
    
    valid_fields = ['visible_when_closed', 'open_for_answering', 'score_correction']
    if field_name not in valid_fields:
        messages.error(request, "Invalid field")
        return redirect(reverse('course_list'))
    
    current_value = getattr(course, field_name)
    setattr(course, field_name, not current_value)
    course.save()
    
    field_display_names = {
        'visible_when_closed': 'Visible when closed',
        'open_for_answering': 'Open for answering', 
        'score_correction': 'Score correction'
    }
    
    messages.success(request, 
        f"{field_display_names[field_name]} {'enabled' if not current_value else 'disabled'}")
    
    return redirect(reverse('course_list'))