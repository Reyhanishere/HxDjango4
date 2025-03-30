from django.urls import path

from .views import *


urlpatterns = [
    path('calculi/pedi_w_zscore/', CalculateWeightZScoreView.as_view(), name='cal_wzs'),
    path('calculi/pedi_l_zscore/', CalculateLengthZScoreView.as_view(), name='cal_lzs'),
    path('calculi/pedi_hc_zscore/', CalculateHCZScoreView.as_view(), name='cal_hczs'),
    path('calculi/pedi_bmi_zscore/', CalculateBMIZScoreView.as_view(), name='cal_bmizs'),

    path('calculi/<slug:link>_page/', calculi_page_view, name='calculi_page'),

    path('calculi/like/', like_calculi, name='calculi_like'),
    
]