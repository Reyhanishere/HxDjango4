from django.urls import path

from .views import *


urlpatterns = [
    path('light/', cases_main, name='cases_main_light'),
    path('', cases_main_tw, name='cases_main'),

    path('hx/cc_tot_ai/', cc_tot_ai, name='cc_tot_ai'),
    path('hx/pi_que_ai/', pi_que_ai, name='pi_que_ai'),
    path('hx/ros_ai/', ros_ai, name='ros_ai'),
    path('hx/phe_ai/', phe_ai, name='phe_ai'),
    
    path("picasso/", PicassoListView.as_view(), name="picasso_list"),
    path("picasso/<slug:slug>/", PicassoDetailView.as_view(), name="picasso_detail"),
    path("picasso/new", PicassoCreateView.as_view(), name="picasso_new"),
    path("picasso/<slug:slug>/edit", PicassoUpdateView.as_view(), name="picasso_edit"),
    path("picasso/<slug:slug>/delete", PicassoDeleteView.as_view(), name="picasso_delete"),
    # path("hx/", CasesListView.as_view(), name="hx_list"),
    path("hx/", cases_list_vv, name="hx_list"),
    path("hx/<slug:slug>/", CaseDetailView.as_view(), name="hx_detail"),
    # path("hx/<slug:slug>/presentation",CasePresentationView.as_view(),  name="hx_presentation"),
    path("hx/<slug:case_slug>/graphs/new", CaseGraphCreateView.as_view(), name="hx_graph_new"),
    path("hx/<slug:case_slug>/graphs/<int:pk>/edit", GraphUpdateView.as_view(), name="hx_graph_edit"),
    path("hx/<slug:case_slug>/graphs/<int:pk>/delete", GraphDeleteView.as_view(), name="hx_graph_delete"),
    path("hx/<slug:slug>/graphs/", GraphListView.as_view(), name="hx_graphs"),
    path("hx/<slug:slug>/presentation",CasePresentationView.as_view(),  name="hx_presentation"),
    path("hx/<slug:slug>/edit", CaseUpdateView.as_view(), name="hx_edit"),
    path("hx/<slug:slug>/delete", CaseDeleteView.as_view(), name="hx_delete"),
    path("hx/<slug:slug>/public",CasePublication.as_view(), name="hx_public"),
    path("hx/new", CaseCreateView.as_view(), name="hx_new"),
    path("search/", SearchResultsListView.as_view(), name="search_results"),
    path("success/", SuccessPageView.as_view(), name="success"),
    path('hx/<slug:case_slug>/add-image', CaseImageCreateView.as_view(), name='hx_add_image'), # Free adding new/old
    path('hx/<slug:case_slug>/add-image/<str:when>', CaseImageCreateView.as_view(), name='hx_add_image_when'), # Set time of the record in the URL
    path('hx/<slug:case_slug>/image-<int:pk>/edit', ImageCaseEditView.as_view(), name='hx_edit_image'),
    path('hx/<slug:case_slug>/image-<int:pk>/delete', ImageCaseDeleteView.as_view(), name='hx_delete_image'),
    path("ex/", ExListView.as_view(), name="ex_list"),
    path("ex/<slug:slug>/", ExDetailView.as_view(), name="ex_detail"),
    path("ex/new", ExCreateView.as_view(), name="ex_new"),
    path("ex/<slug:slug>/edit", ExUpdateView.as_view(), name="ex_edit"),
    path("ex/<slug:slug>/delete", ExDeleteView.as_view(), name="ex_delete"),
    path('like/', like_comment, name='like_comment'),
    path('add_reply/', add_reply, name='add_reply'),

    path('uni_hx/new/choose/', hx_new_choose_view, name='hx_new_choose'),

    path('uni_hx/new/<str:page>/', CaseNewPageView.as_view(), name='unicase_new'), # Create mode (first page)
    path('uni_hx/<slug:slug>/edit/<str:page>/', CaseNewPageView.as_view(), name='unicase_page'), # Update mode
]

