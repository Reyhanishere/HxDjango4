from itertools import chain

from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse

from django.db.models import Q

from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Case, Picasso, FollowUp, Comment, ImageCase, Note, Reply
from .forms import (
    CaseCreateForm,
    CaseUpdateForm,
    # FollowUpForm,
    CommentForm,
    PicassoCreateForm,
    PicassoUpdateForm,
    # LabTestForm,
    CaseImageForm,
    ExCreateForm,
    ExUpdateForm,
    ReplyForm,
)


class CasesListView(ListView):
    model = Case
    template_name = "hx_list.html"


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
        return render(request, 'hx_detail.html', context)

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
    success_url = reverse_lazy("hx_list")
    form_class = CaseUpdateForm

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
    # formset = LabTestForm
    # fields = (
    #     "title",
    #     "rts",
    #     "description",
    #     "pretext",
    #     "gender",
    #     "location",
    #     "job",
    #     "dwelling",
    #     "age",
    #     "marriage",
    #     "doctor",
    #     "source",
    #     "reliability",
    #     "setting",
    #     "cc",
    #     "pi",
    #     "pmh",
    #     "drg",
    #     "sh",
    #     "fh",
    #     "alg",
    #     "ros",
    #     "phe",
    #     "dat",
    #     "summary",
    #     "ddx",
    #     "pdx",
    #     "act",
    #     "post_text",
    #     "tags",
    #     "slug",
    #     "suggests",
    # )

    success_url = "/cases/success/"

    # def get_success_url(self):
    #     case = self.get_object()
    #     return case.slug #reverse("hx_detail", kwargs={"slug": case.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         data["formset"] = LabTestForm(self.request.POST)
    #     else:
    #         data["formset"] = LabTestForm()
    #     print(data["formset"])  # Add this line to check formset contents
    #     return data


class CaseImageView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ImageCase
    form_class = CaseImageForm
    template_name = "hx_add_img.html"
    success_url = "/cases/success/"

    def form_valid(self, form):
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        form.instance.case = case
        return super().form_valid(form)
    def test_func(self):  # new
        case_slug = self.kwargs["case_slug"]
        case = get_object_or_404(Case, slug=case_slug, author=self.request.user)
        return case.author == self.request.user


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

    def form_valid(self, form):  # new
        form.instance.author = self.request.user
        return super().form_valid(form)


class PicassoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picasso
    template_name = "picasso_edit.html"
    success_url = reverse_lazy("picasso_list")
    # how to show a message
    form_class = PicassoUpdateForm

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
        "-date_created"
    )[:4]
    return render(
        request, "cases_main.html", {"hxs": hxs, "picassos": picassos, "exs": exs}
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

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ExUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    template_name = "ex/ex_edit.html"
    success_url = reverse_lazy("ex_list")
    # how to show a message
    form_class = ExUpdateForm

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


# class LabTestCreateView(CreateView):
#     model = LabTestItem
#     form_class = LabTestForm
#     template_name = "labtest_create.html"
#     success_url = "cases/success"  # Update with your success URL
