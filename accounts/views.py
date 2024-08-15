from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
import cases.models as Cases

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"

@login_required
def self_user_cases(request):
    user = request.user
    hxs = Cases.Case.objects.filter(author=user).order_by("-date_created")
    return render(request, 'user/self_user_cases.html', {'hxs': hxs,})

