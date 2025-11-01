from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import *
import cases.models as Cases
import steps.models as Steps
from .models import *


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

@login_required
def self_user_cases(request):
    user = request.user
    hxs = Cases.Case.objects.filter(author=user).order_by("-date_created")
    return render(request, 'user/self_user_cases.html', {'hxs': hxs,})

@login_required
def self_user_courses(request):
    user = request.user
    courses = Steps.CourseRegistration.objects.filter(student=user).order_by("-joined_at")
    for course in courses:
        print(course.course.title)
    return render(request, 'user/self_user_courses.html', {'courses': courses,})

class UserChangeInfoView(LoginRequiredMixin, UpdateView):
    model= CustomUser
    template_name='registration/change_info.html'
    form_class=CustomUserChangeForm
    success_url=reverse_lazy('self_user_cases')
    def get_object(self, queryset=None):
        return self.request.user


def dashboard(request):
    return render(request, "user/dashboard.html")

def verification_pending(request):
    try:
        request.user.student_profile
        if request.user.student_profile.verified:
            return redirect("dashboard")
        elif not request.user.student_profile.completed:
            return redirect("fill_user_profile")
        else:
            return render(request, "user/verification_pending.html")
    except:
        return redirect("new_user_profile")
        
    
def my_profile(request):
    if request.user.student_profile.verified:
        return redirect("dashboard")
    # elif request.user.student_profile.completed:
    #     pass
    else:
        return redirect("new_user_profile")
    

class StudentProfileCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = StudentProfile
    template_name = "user/student_profile_new.html"
    form_class = StudentProfileCreateForm
    success_url=reverse_lazy('profile_verification_pending')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.completed = True
        return super().form_valid(form)
    
    def test_func(self):
        return not self.request.user.has_profile()
