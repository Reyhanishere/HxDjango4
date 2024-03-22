from django.urls import path

from .views import (CasesListView,
                     CaseDetailView, 
                     CaseUpdateView, 
                     CaseDeleteView, 
                     CaseCreateView,
                     cases_main,
                     PicassoCreateView,
                     PicassoUpdateView,
                     PicassoListView,
                     PicassoDetailView,
                     )


urlpatterns = [
    path('', cases_main, name='cases_main'),
    path("picasso/", PicassoListView.as_view(), name="picasso_list"),
    path("picasso/<slug:slug>/", PicassoDetailView.as_view(), name="picasso_detail"),
    path("picasso/new", PicassoCreateView.as_view(), name="picasso_new"),
    path("picasso/<slug:slug>/edit", PicassoUpdateView.as_view(), name="picasso_edit"),
    path("hx/", CasesListView.as_view(), name="hx_list"),
    path("hx/<slug:slug>/", CaseDetailView.as_view(), name="hx_detail"),
    path("hx/<slug:slug>/edit", CaseUpdateView.as_view(), name="hx_edit"),
    path("hx/<slug:slug>/delete", CaseDeleteView.as_view(), name="hx_delete"),
    path("hx/new", CaseCreateView.as_view(), name="hx_new"),
    ]

