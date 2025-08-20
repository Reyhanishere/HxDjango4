from django.urls import path
from .views import *

urlpatterns = [
    path('mono/',mono_text_check , name='mono_text_check'),
]