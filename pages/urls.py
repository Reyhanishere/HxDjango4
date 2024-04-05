from django.urls import path
from .views import HomePageView, AboutPageView, TermsPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("terms/", TermsPageView.as_view(), name="terms"),
]
