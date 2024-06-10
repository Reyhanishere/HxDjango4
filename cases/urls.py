from django.urls import path

from .views import *


urlpatterns = [
    path('', cases_main, name='cases_main'),
    path("picasso/", PicassoListView.as_view(), name="picasso_list"),
    path("picasso/<slug:slug>/", PicassoDetailView.as_view(), name="picasso_detail"),
    path("picasso/new", PicassoCreateView.as_view(), name="picasso_new"),
    path("picasso/<slug:slug>/edit", PicassoUpdateView.as_view(), name="picasso_edit"),
    path("picasso/<slug:slug>/delete", PicassoDeleteView.as_view(), name="picasso_delete"),
    path("hx/", CasesListView.as_view(), name="hx_list"),
    path("hx/<slug:slug>/", CaseDetailView.as_view(), name="hx_detail"),
    # path("hx/<slug:slug>/presentation",CasePresentationView.as_view(),  name="hx_presentation"),
    path("hx/<slug:case_slug>/graphs/new", CaseGraphCreateView.as_view(), name="hx_graph_new"),
    path("hx/<slug:case_slug>/graphs/", GraphListView.as_view(), name="hx_graphs"),
    path("hx/<slug:slug>/presentation",CasePresentationView.as_view(),  name="hx_presentation"),
    path("hx/<slug:slug>/edit", CaseUpdateView.as_view(), name="hx_edit"),
    path("hx/<slug:slug>/delete", CaseDeleteView.as_view(), name="hx_delete"),
    path("hx/new", CaseCreateView.as_view(), name="hx_new"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    # path('hx/new/lab', LabTestCreateView.as_view(), name='lab-create'),
    path("success/", SuccessPageView.as_view(), name="success"),
    path('hx/<slug:case_slug>/add-image', CaseImageView.as_view(), name='hx_add_image'),
    path("ex/", ExListView.as_view(), name="ex_list"),
    path("ex/<slug:slug>/", ExDetailView.as_view(), name="ex_detail"),
    path("ex/new", ExCreateView.as_view(), name="ex_new"),
    path("ex/<slug:slug>/edit", ExUpdateView.as_view(), name="ex_edit"),
    path("ex/<slug:slug>/delete", ExDeleteView.as_view(), name="ex_delete"),
    path('like/', like_comment, name='like_comment'),
    path('add_reply/', add_reply, name='add_reply'),
    ]
