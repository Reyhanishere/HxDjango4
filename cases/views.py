from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy, reverse
from django.shortcuts import render

from .models import Case, Picasso, FollowUp, Comment
from .forms import (CaseUpdateForm,
                    # FollowUpForm, 
                    CommentForm,
                    PicassoCreateForm,
                    PicassoUpdateForm,
                    )


class CasesListView(ListView):
    model = Case
    template_name = 'hx_list.html'

class CommentGet(DetailView): # new
    model = Case
    template_name = "hx_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView): # new
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
    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)
    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    

class CaseUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Case
    # fields="__all__"
    template_name = 'hx_edit.html'
    success_url = reverse_lazy("hx_list")
    form_class = CaseUpdateForm
    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user

class CaseDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Case
    template_name = 'hx_delete.html'
    success_url = "/cases/hx"
    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user


class CaseCreateView(LoginRequiredMixin, CreateView): # new
    model = Case
    template_name = "hx_new.html"
    fields=("title","cat","description","pretext","gender","location","job",
            "dwelling", "age", "marriage", "doctor", "source", "reliability",
            "setting", "PR","BP_S","BP_D","RR", "SPO2_O","SPO2_N","Temp",
            "cc","pi","pmh","drg", "sh", "fh", "alg","ros","phe", "dat",
              "summary","ddx", "pdx", "act","post_text","picasso", "slug")
    success_url = reverse_lazy("cases_main")
    
    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)


class PicassoListView(ListView):
    model = Picasso
    template_name = 'picasso_list.html'

class PicassoDetailView(DetailView):
    model = Picasso
    template_name = "picasso_detail.html"

class PicassoCreateView(LoginRequiredMixin, CreateView):
    model=Picasso
    template_name = "picasso_new.html"
    # fields=("title","image","description","text","slug")
    form_class = PicassoCreateForm

    def form_valid(self, form): # new
        form.instance.author = self.request.user
        return super().form_valid(form)

class PicassoUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Picasso
    template_name = 'picasso_edit.html'
    success_url = reverse_lazy("picasso_list")
    # how to show a message
    form_class = PicassoUpdateForm
    def test_func(self): # new
        obj = self.get_object()
        return obj.author == self.request.user


def cases_main(request):
    hxs = Case.objects.filter(verified=True).order_by('-date_created')[:3]
    picassos = Picasso.objects.filter(verified=True).order_by('-date_created')[:3]
    return render(request, 'cases_main.html', {'hxs': hxs, 'picassos': picassos})
