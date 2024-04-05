from django.urls import path
from .views import DocsListView, DocDetailView

urlpatterns = [
    path("",DocsListView.as_view(),name="docs_list"),
    path("<int:pk>/",DocDetailView.as_view(), name="doc_detail"),
]
