from django.urls import path
from .views import HomePageView, AboutPageView, TermsPageView, GraphsPageView, PremiumPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("terms/", TermsPageView.as_view(), name="terms"),
    path("cases/graphs/", GraphsPageView.as_view(), name="graphs"),
    path("premium/", PremiumPageView.as_view(), name="premium"),

   
]
