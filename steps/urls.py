from django.urls import path
from .views import *

urlpatterns = [
    path('', StepListView.as_view(), name='step_list'),
    path('step/<slug:slug>/', StepDetailView.as_view(), name='step_detail'),
    path('blocks/<int:block_id>/submit/', submit_answer, name='submit_answer'),
]