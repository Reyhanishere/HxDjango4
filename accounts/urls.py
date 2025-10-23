from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", self_user_cases, name="self_user_cases"),
    path("courses/", self_user_courses, name="self_user_courses"),

    path("change/<int:pk>/", UserChangeInfoView.as_view(), name="change_user_info"),

]
