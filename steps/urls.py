from django.urls import path
from .views import *

urlpatterns = [
    path('', StepListView.as_view(), name='step_list'),
    path('race/<int:pk>/', StepRaceDetailView.as_view(), name='step_race_detail'),
    path('step/<slug:slug>/', StepDetailView.as_view(), name='step_detail'),
    
    path('interactive_step/<int:step_id>/blocks/<int:block_number>/', load_interactive_block, name='get_block'),
    path('interactive_step/<slug:slug>/', InteractiveStepDetailView.as_view(), name='interactive_step_detail'),
    path('interactive_step/<slug:slug>/graph_code/', InteractiveStepGraphVizz.as_view(), name='interactive_step_graph_code'),

    
    path('submit_race_score/<int:race_id>/', submit_race_score, name='submit_race_score'),

    path('race/<int:race_id>/ranking/', ranking_page, name='ranking_page'),
    path('race/<int:race_id>/my_rank/<str:id_score>/', my_rank, name='my_rank'),

    path('blocks/<int:block_id>/submit/', submit_answer, name='submit_answer'),

    path('course/<uuid:uuid>/', course_detail, name='course_detail'),
    path('course/<uuid:uuid>/register/', course_register, name='course_register'),
    path('course/<uuid:uuid>/race/<int:race_id>/', StepCourseRaceDetailView.as_view(), name='course_race_view'),
    path('course/<uuid:uuid>/race/<int:race_id>/submit_race_score/', submit_course_race_score, name='submit_course_race_score'),

    path('course/<uuid:course_uuid>/toggle/<str:field_name>/', toggle_course_field, name='toggle_field'),
]



