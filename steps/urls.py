from django.urls import path
from .views import *

urlpatterns = [
    path('', StepListView.as_view(), name='step_list'),
    path('race/<int:pk>/', StepRaceDetailView.as_view(), name='step_race_detail'),
    path('step/<slug:slug>/', StepDetailView.as_view(), name='step_detail'),
    
    path('interactive_step/<int:step_id>/blocks/<int:block_number>/', load_interactive_block, name='get_block'),
    path('interactive_step/<slug:slug>/', InteractiveStepDetailView.as_view(), name='interactive_step_detail'),
    
    path('submit_race_score/<int:race_id>/', submit_race_score, name='submit_race_score'),
    path('race/<int:race_id>/ranking/', ranking_page, name='ranking_page'),
    path('blocks/<int:block_id>/submit/', submit_answer, name='submit_answer'),
]

