from itertools import chain
import requests
import json, math

from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.conf import settings

from django.db.models import Q

from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *
from .utils import *
from .decorators import *



class CasesListView(ListView):
    model = Case
    template_name = "hx_list.html"

def cases_list_vv(request):
    cases = Case.objects.filter(visible=True, verified=True).order_by('-date_created')
    return render(request, 'hx_list.html', {'case_list': cases})

class CommentGet(DetailView):  # new
    model = Case
    template_name = "hx_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):  # new
    model = Case
    form_class = CommentForm
    template_name = "hx_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        comment.case = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        case = self.get_object()
        return reverse("hx_detail", kwargs={"slug": case.slug})


class CaseDetailView(View):
    # def get(self, request, *args, **kwargs):
    #     view = CommentGet.as_view()
    #     return view(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     view = CommentPost.as_view()
    #     return view(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):  # new
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = CommentForm()
    #     return context
    def get(self, request, *args, **kwargs):
        case = Case.objects.get(slug=kwargs.get('slug'))
        comments = Comment.objects.filter(case=case)
        context = {'case': case, 'comments': comments, 'comment_form': CommentForm(), 'reply_form': ReplyForm()}
        if case.is_pedi:
            tmplt_name = "hx/hx_detail_pedi.html"
        else:
            tmplt_name = "hx/hx_detail.html"
        return render(request, tmplt_name, context)
        
    def post(self, request, *args, **kwargs):
        case_slug = kwargs.get('slug')
        case = Case.objects.get(slug=case_slug)
        comment_form = CommentForm(request.POST)
        reply_form = ReplyForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.case = case
            comment.author = request.user
            comment.save()
            return redirect(reverse('hx_detail', kwargs={'slug': case_slug}))
        elif reply_form.is_valid():
            reply = reply_form.save(commit=False)
            comment_id = request.POST.get('comment_id')
            reply.comment = Comment.objects.get(id=comment_id)
            reply.author = request.user
            reply.save()
            return redirect(reverse('hx_detail', kwargs={'slug': case_slug}))
        else:
            return redirect(reverse('hx_detail', kwargs={'slug': case_slug}))
        
def add_reply(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        reply_content = request.POST.get('reply_content')
        if comment_id and reply_content:
            comment = get_object_or_404(Comment, id=comment_id)
            reply = Reply(content=reply_content, comment=comment, author=request.user)
            reply.save()
            # Redirect back to the case detail page with the appropriate slug
            return redirect('hx_detail', slug=comment.case.slug)
    # Handle invalid or GET requests by redirecting to the home page
    return redirect('hx_detail', slug=comment.case.slug)  # Adjust the redirect URL as needed

def like_comment(request):
    if request.method == 'POST':
        user = request.user
        comment_id = request.POST.get('comment_id')
        if comment_id:
            try:
                comment = Comment.objects.get(id=comment_id)
                if user in comment.liked_by.all():
                    # User has already liked the comment, remove their like
                    comment.liked_by.remove(user)
                    comment.likes -= 1
                    comment.save()
                    return JsonResponse({'likes': comment.likes, 'liked': False})
                else:
                    # User hasn't liked the comment yet, add their like
                    comment.liked_by.add(user)
                    comment.likes += 1
                    comment.save()
                    return JsonResponse({'likes': comment.likes, 'liked': True})
            except Comment.DoesNotExist:
                pass
    return JsonResponse({'error': 'Invalid request'}, status=400)

class CaseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Case
    # fields="__all__"
    template_name = "hx_edit.html"
    form_class = CaseUpdateForm

    def get_success_url(self):
        case_slug = self.kwargs["slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Case
    template_name = "hx_delete.html"
    success_url = "/cases/hx"

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class CaseCreateView(LoginRequiredMixin, CreateView):  # new
    model = Case
    template_name = "hx_new.html"
    form_class = CaseCreateForm
    success_url = reverse_lazy("self_user_cases")

    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def get_when(when):
    if when == 'old': return True
    elif when == 'new': return False
    elif when == None: return None
    else: raise Http404()
    
class CaseImageCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ImageCase
    form_class = CaseImageForm
    template_name = "hx_add_img.html"
            
    def get_initial(self):
        initial = super().get_initial()
        when = self.kwargs.get('when')
        initial['is_old'] = get_when(when)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        when = self.kwargs.get('when')
        kwargs['is_old'] = get_when(when)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        when = self.kwargs.get('when')
        context['is_old'] = get_when(when)
        return context
    
    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/"
    
    def form_valid(self, form):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        form.instance.case = case
        when = self.kwargs.get('when')
        form.instance.is_old = get_when(when)
        return super().form_valid(form)
    def test_func(self):  # new
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        return case.author == self.request.user

class ImageCaseEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model=ImageCase
    form_class=ImageCaseEditForm
    template_name="hx/image_case_edit.html"
    def test_func(self):
        img_id=self.kwargs["pk"]
        img=get_object_or_404(ImageCase, id=img_id)
        return img.case.author == self.request.user
    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/"

class ImageCaseDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model=ImageCase
    template_name="hx/image_case_delete.html"
    def test_func(self):
        img_id=self.kwargs["pk"]
        img=get_object_or_404(ImageCase, id=img_id)
        return img.case.author == self.request.user
    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/"


class CasePresentationView(DetailView):
    model = Case

    def get_template_names(self):
        case = self.get_object()

        if case.is_pedi:
            return ["hx/hx_prsnt_pdtr.html"]
        else:
            return ["hx_presentation.html"]

class PicassoListView(ListView):
    model = Picasso
    template_name = "picasso_list.html"


class PicassoDetailView(DetailView):
    model = Picasso
    template_name = "picasso_detail.html"


class PicassoCreateView(LoginRequiredMixin, CreateView):
    model = Picasso
    template_name = "picasso_new.html"
    # fields=("title","image","description","text","slug")
    form_class = PicassoCreateForm
    success_url = reverse_lazy("picasso_list")
    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class PicassoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picasso
    template_name = "picasso_edit.html"
    # how to show a message
    form_class = PicassoUpdateForm
    def get_success_url(self):
        pic_slug = self.kwargs["slug"]
        pic = get_object_or_404(Picasso, slug=pic_slug)
        return f"/cases/picasso/{pic.slug}/"

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class PicassoDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picasso
    template_name = "picasso_delete.html"
    fields = ["delete"]

    def test_func(self):  # new
        obj = self.get_object()
        return obj.author == self.request.user


class SuccessPageView(TemplateView):
    template_name = "pages/success.html"


def cases_main(request):
    hxs = Case.objects.filter(verified=True, visible=True).order_by("-date_created")[:4]
    picassos = Picasso.objects.filter(
        verified=True, delete=False, visible=True
    ).order_by("-date_created")[:3]
    exs = Note.objects.filter(verified=True, delete=False, visible=True).order_by(
        "-date_created")[:4]
    return render(
        request, "cases_main.html", {"hxs": hxs, "picassos": picassos, "exs": exs}
    ) 

def cases_main_tw(request):
    hxs = Case.objects.filter(verified=True, visible=True).order_by("-date_created")[:3]
    picassos = Picasso.objects.filter(
        verified=True, delete=False, visible=True
    ).order_by("-date_created")[:6]
    # time_est_pic=[]
    # for pic in picassos:
    #     pic_words=pic.text.split()
    #     time_est_pic.append(round(len(pic_words)/200))

    exs = Note.objects.filter(verified=True, delete=False, visible=True).order_by(
        "-date_created")[:3]
    
    # time_est_ex=[]
    # for ex in exs:
    #     ex_words=ex.text.split()
    #     time_est_ex.append(round(len(pic_words)/200))
    return render(
        request, "./pages/cases_main_tw.html", {"hxs": hxs, "picassos": picassos, "exs": exs}
    )


class SearchResultsListView(ListView):
    model = Case
    context_object_name = "case_list"
    template_name = "pages/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            # Create Q objects for each field to search in both models
            q_objects_model1 = Q()
            q_objects_model2 = Q()
            q_objects_model3 = Q()

            for field in Case._meta.fields:
                if field.get_internal_type() in ["CharField", "TextField"]:
                    q_objects_model1 |= Q(**{f"{field.name}__icontains": query})
            for field in Picasso._meta.fields:
                if field.get_internal_type() in ["CharField", "TextField"]:
                    q_objects_model2 |= Q(**{f"{field.name}__icontains": query})
            for field in Note._meta.fields:
                if field.get_internal_type() in ["CharField", "TextField"]:
                    q_objects_model3 |= Q(**{f"{field.name}__icontains": query})

            queryset_model1 = Case.objects.filter(q_objects_model1, verified=True)
            queryset_model2 = Picasso.objects.filter(
                q_objects_model2, verified=True, visible=True, delete=False
            )
            queryset_model3 = Note.objects.filter(
                q_objects_model3, verified=True, visible=True, delete=False
            )

            context = list(chain(queryset_model1, queryset_model2, queryset_model3))
            return context
        else:
            return None


class ExListView(ListView):
    model = Note
    template_name = "ex/ex_list.html"


class ExCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = "ex/ex_new.html"
    success_url = reverse_lazy("ex_list")
    form_class = ExCreateForm
    # def get_success_url(self):
    #     ex_slug = self.kwargs["ex_slug"]
    #     case = get_object_or_404(Case, slug=ex_slug)
    #     return f"/cases/ex/{case.slug}/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ExUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = "ex/ex_edit.html"
    # success_url = reverse_lazy("ex_list")
    # how to show a message
    form_class = ExUpdateForm
    def get_success_url(self):
        ex_slug = self.kwargs["slug"]
        ex = get_object_or_404(Note, slug=ex_slug)
        return f"/cases/ex/{ex.slug}/"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ExDetailView(DetailView):
    model = Note
    template_name = "ex/ex_detail.html"


class ExDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = "ex/ex_delete.html"
    fields = ["delete"]
    success_url = reverse_lazy("ex_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class FreeGraphCreateView(LoginRequiredMixin, CreateView):
    model=LabGraphSelection
    form_class=FreeGraphForm
    template_name=""
    success_url = "/cases/graphs/"
    
class CaseGraphCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model=LabGraphSelection
    form_class=FreeGraphForm # the same as above
    template_name="hx/graph/graph_new.html"

    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/graphs"

    def form_valid(self, form):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        form.instance.case = case
        form.instance.author=self.request.user
        return super().form_valid(form)
    def test_func(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        return case.author == self.request.user

class GraphListView(DetailView):
    model=Case
    template_name="hx/graph/graph_list.html"

class GraphUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LabGraphSelection
    template_name = "hx/graph/graph_edit.html"
    # how to show a message
    form_class = GraphUpdateForm

    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/graphs"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class GraphDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model=LabGraphSelection
    template_name="hx/graph/graph_delete.html"

    def get_success_url(self):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug)
        return f"/cases/hx/{case.slug}/graphs"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class CasePublication(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model= Case
    template_name='hx_edit.html'
    form_class=CasePubForm
    success_url = reverse_lazy("self_user_cases")
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

def cc_tot_ai(request):
    API_URL='https://api.metisai.ir/api/v1'
    SESSION_CODE='47f58cce-ed0b-4b77-9ff3-ef5cf457eab4'
    Headers={
    'Authorization':settings.AI_API_KEY,
    'content-type':'application/json'
    }
    use_limit=100
    if request.user.is_authenticated and request.user.hx_cc_ai_permission and request.user.hx_cc_ai_use_count<use_limit:
        if request.method == 'POST':
            symptom = request.POST.get('cc_fa')
            if len(symptom)>3:
                Data = {
                'message':{
                    'content': f"{symptom}",
                    'type':'USER'
                    },
                }
                message_url = f'{API_URL}/chat/session/{SESSION_CODE}/message'
                response = requests.post(message_url, headers=Headers, data=json.dumps(Data))
            else:
                return JsonResponse({'error': 'Enter Chief Complaint First!'}, status=400)

            if response.status_code == 200:
                cct_ai_response = response.json().get('content')
                request.user.hx_cc_ai_use_count+=1
                request.user.save()
                new_log = AIReqResLog(
                    user=request.user,
                    request_content=Data["message"]['content'],
                    ai_model="CC",
                    response_content=cct_ai_response,
                )
                new_log.save()

                return JsonResponse({'cct_ai_response': cct_ai_response})
            else:
                return JsonResponse({'error': 'API call failed'}, status=500)
    elif request.user.is_authenticated and request.user.hx_cc_ai_permission and request.user.hx_cc_ai_use_count>use_limit:
        return JsonResponse({'error': f'You have exceeded use limit.({use_limit})'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def pi_que_ai(request):
    API_URL='https://api.metisai.ir/api/v1'
    SESSION_CODE='2ac615db-1eb4-43d0-8630-8dc23c3f1f2f'
    Headers={
    'Authorization':settings.AI_API_KEY,
    'content-type':'application/json'
    }
    use_limit=100
    if request.user.is_authenticated and request.user.hx_pi_ai_permission and request.user.hx_pi_ai_use_count<use_limit:
        if request.method == 'POST':
            symptom = request.POST.get('cc_term')
            incomplete_pi = request.POST.get('incomplete_pi')
            
            if len(symptom)>3:
                Data = {
                'message':{
                    'content': f"CC: {symptom}\n PI till now: {incomplete_pi}",
                    'type':'USER'
                    },
                }
                message_url = f'{API_URL}/chat/session/{SESSION_CODE}/message'
                response = requests.post(message_url, headers=Headers, data=json.dumps(Data))
            else:
                return JsonResponse({'error': 'Enter Chief Complaint First!'}, status=400)

            if response.status_code == 200:
                piq_ai_response = response.json().get('content')
                request.user.hx_pi_ai_use_count+=1
                request.user.save()
                new_log = AIReqResLog(
                    user=request.user,
                    request_content=Data["message"]['content'],
                    ai_model="PI",
                    response_content=piq_ai_response,
                )
                new_log.save()

                return JsonResponse({'piq_ai_response': piq_ai_response})
            else:
                return JsonResponse({'error': 'API call failed'}, status=500)
    elif request.user.is_authenticated and request.user.hx_pi_ai_permission and request.user.hx_pi_ai_use_count>use_limit:
        return JsonResponse({'error': f'You have exceeded use limit.({use_limit})'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def ros_ai(request):
    API_URL='https://api.metisai.ir/api/v1'
    SESSION_CODE= 'c67fd155-0221-45ef-8e7d-a6e64711cfe1'
    Headers={
    'Authorization':settings.AI_API_KEY,
    'content-type':'application/json'
    }
    use_limit=60
    if request.user.is_authenticated and request.user.hx_ros_ai_permission and request.user.hx_ros_ai_use_count<use_limit: ###
        if request.method == 'POST':
            cc = request.POST.get('cc')
            pi = request.POST.get('pi')
            if request.POST.get('pmh'):
                pmh = request.POST.get('pmh')
            else:
                pmh='None'

            if request.POST.get('dh'):
                dh = request.POST.get('dh')
            else:
                dh='None'

            if request.POST.get('fh'):
                fh = request.POST.get('fh')
            else:
                fh='None'            
            if request.POST.get('sh'):
                sh = request.POST.get('sh')
            else:
                sh='None'            
            
            if request.POST.get('ah'):
                ah = request.POST.get('ah')
            else:
                ah='None'

            content=f"CC: {cc}\nPI:\n{pi}\n\nPMH:\n{pmh}\n\nDH:\n{dh}\n\nFH:\n{fh}\n\nSH:\n{sh}\n\nAH:\n{ah}"

            if len(cc)<4:
                return JsonResponse({'error': 'Enter Proper Chief Complaint First!'}, status=400)

            elif len(pi.split())<10:
                return JsonResponse({'error': 'Enter Proper Present Illness (PI)!'}, status=400)

            else:
                Data = {
                'message':{
                    'content': content,
                    'type':'USER'
                    },
                }
                message_url = f'{API_URL}/chat/session/{SESSION_CODE}/message'
                response = requests.post(message_url, headers=Headers, data=json.dumps(Data))

            if response.status_code == 200:
                ros_ai_response = response.json().get('content')
                request.user.hx_ros_ai_use_count+=1
                request.user.save()
                new_log = AIReqResLog(
                    user=request.user,
                    request_content=Data["message"]['content'],
                    ai_model="ROS",
                    response_content=ros_ai_response,
                )
                new_log.save()

                return JsonResponse({'ros_ai_response': ros_ai_response})
            else:
                return JsonResponse({'error': 'API call failed'}, status=500)
    elif request.user.is_authenticated and request.user.hx_ros_ai_permission and request.user.hx_ros_ai_use_count>use_limit:
        return JsonResponse({'error': f'You have exceeded use limit.({use_limit})'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def phe_ai(request):
    API_URL='https://api.metisai.ir/api/v1'
    SESSION_CODE= '928ef5bc-6085-4915-be28-9486eb075f06'
    Headers={
    'Authorization':settings.AI_API_KEY,
    'content-type':'application/json'
    }
    use_limit=60
    if request.user.is_authenticated and request.user.hx_phe_ai_permission and request.user.hx_phe_ai_use_count<use_limit: ###
        if request.method == 'POST':
            cc = request.POST.get('cc')
            pi = request.POST.get('pi')
            if request.POST.get('pmh'):
                pmh = request.POST.get('pmh')
            else:
                pmh='None'

            if request.POST.get('dh'):
                dh = request.POST.get('dh')
            else:
                dh='None'

            if request.POST.get('fh'):
                fh = request.POST.get('fh')
            else:
                fh='None'            
            if request.POST.get('sh'):
                sh = request.POST.get('sh')
            else:
                sh='None'            
            
            if request.POST.get('ah'):
                ah = request.POST.get('ah')
            else:
                ah='None'

            content=f"CC: {cc}\nPI:\n{pi}\n\nPMH:\n{pmh}\n\nDH:\n{dh}\n\nFH:\n{fh}\n\nSH:\n{sh}\n\nAH:\n{ah}"

            if len(cc)<4:
                return JsonResponse({'error': 'Enter Proper Chief Complaint First!'}, status=400)

            elif len(pi.split())<10:
                return JsonResponse({'error': 'Enter Proper Present Illness (PI)!'}, status=400)

            else:
                Data = {
                'message':{
                    'content': content,
                    'type':'USER'
                    },
                }
                message_url = f'{API_URL}/chat/session/{SESSION_CODE}/message'
                response = requests.post(message_url, headers=Headers, data=json.dumps(Data))

            if response.status_code == 200:
                phe_ai_response = response.json().get('content')
                request.user.hx_phe_ai_use_count+=1
                request.user.save()
                new_log = AIReqResLog(
                    user=request.user,
                    request_content=Data["message"]['content'],
                    ai_model="PhE",
                    response_content=phe_ai_response,
                )
                new_log.save()

                # return JsonResponse({'phe_ai_response': phe_ai_response})
                return JsonResponse({'phe_ai_response': phe_ai_response})
            
            else:
                return JsonResponse({'error': 'API call failed'}, status=500)
    elif request.user.is_authenticated and request.user.hx_phe_ai_permission and request.user.hx_phe_ai_use_count>use_limit:
        return JsonResponse({'error': f'You have exceeded use limit.({use_limit})'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


class HxNewChooseView(TemplateView):
    template_name = "hx/hx_new_choose.html"

@student_profile_state
def hx_new_choose_view(request):
    return render(request, 'hx/hx_new_choose.html', None)


PAGES_FLOW = ['cc_id', 'pi', 'pmh', 'dsf', 'ros_phe', 'last_fields', 'select_prof']
PAGES = {'cc_id':'CC & ID', 'pi':'Present Illness', 'pmh':'Past Medical', 'dsf':'Drugs Social Family', 'ros_phe':'ROS & PhE', 'last_fields':'Actions & Dx', 'select_prof':'Professor'}


class CaseNewPageView(View):
    model = Case

    def get_object(self):
        """Return the case object if pk exists, otherwise None."""
        slug = self.kwargs.get('slug')
        if slug:
            return get_object_or_404(Case, slug=slug, author=self.request.user)
        return None

    def get_form_class(self, page):
        if page == 'cc_id':
            return CaseCCAndIDForm
        elif page == 'pi':
            return CasePIForm
        elif page == 'pmh':
            return CasePMHForm
        elif page == 'dsf':
            return CaseDSFForm
        elif page == 'ros_phe':
            return CaseROSPhEForm
        elif page == 'last_fields':
            return CaseLastFieldsForm
        elif page == 'select_prof':
            return CaseSelectProfForm
        raise Http404("Invalid page")

    def get(self, request, page, slug=None):
        obj = self.get_object()
        form_class = self.get_form_class(page)
        form = form_class(instance=obj) if form_class else None
        index = PAGES_FLOW.index(page)
        try:
            if obj.slug:
                exists=True
        except:
            exists=False
            
        context = {
            'object': obj,
            'form': form,
            'page_name': page,
            'has_prev': index > 0,
            'has_next': index < len(PAGES_FLOW) - 1,
            'pages': PAGES,
            'exists': exists,
        }

        return render(request, f'hx/case_page_{page}.html', context)
    
    def post(self, request, page, slug=None):
        obj = self.get_object()
        form_class = self.get_form_class(page)
        form = form_class(request.POST, instance=obj) if form_class else None

        if form and form.is_valid():
            case = form.save(commit=False)
            case.author = request.user
            case.title = case.generate_title()
            case.visible = False
            case.is_university_case = True
            case.save()

            # if this was the first creation, return the new slug to frontend
            if not obj and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'created', 'slug': case.slug})

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'saved'})

            # return redirect('case_step', slug=case.slug, page=self.get_next_step(page))

        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

        # Determine next page
        current_page = page
        page_index = PAGES_FLOW.index(current_page)
        next_page = request.POST.get('next')
        prev_page = request.POST.get('prev')
        submit_page = request.POST.get('submit_final')

        # Case creation special handling
        if not obj and form and form.instance.slug:
            obj = form.instance

        if next_page and page_index + 1 < len(PAGES_FLOW):
            return redirect('unicase_page', slug=obj.slug, page=PAGES_FLOW[page_index + 1])

        if prev_page and page_index > 0:
            return redirect('unicase_page', slug=obj.slug, page=PAGES_FLOW[page_index - 1])
        
        if submit_page:
            case.done = True
            case.save()
            return redirect('hx_detail', slug=obj.slug)

        return redirect('unicase_page', slug=obj.slug, page=current_page)
