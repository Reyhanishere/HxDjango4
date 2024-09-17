from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .forms import *
import cases.models as Cases
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

@login_required
def self_user_cases(request):
    user = request.user
    hxs = Cases.Case.objects.filter(author=user).order_by("-date_created")
    return render(request, 'user/self_user_cases.html', {'hxs': hxs,})

class UserChangeInfoView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model= CustomUser
    template_name='registration/change_info.html'
    form_class=CustomUserChangeForm
    success_url=reverse_lazy('self_user_cases')
    def test_func(self):
        user_id = self.kwargs["pk"]
        user = get_object_or_404(CustomUser, id=user_id)
        return user == self.request.user
