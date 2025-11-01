from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", dashboard, name="dashboard"),
    path("cases/", self_user_cases, name="self_user_cases"),
    path("courses/", self_user_courses, name="self_user_courses"),

    path("change/", UserChangeInfoView.as_view(), name="change_user_info"),
    path("verification_pending/", verification_pending ,name="profile_verification_pending"),
    path("my_profile/", my_profile ,name="user_profile"),
    path("new_profile/", StudentProfileCreateView.as_view() ,name="new_user_profile"),

    

]
