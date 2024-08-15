from django.urls import path
from .views import SignUpView, self_user_cases
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", self_user_cases, name="self_user_cases"),
]
