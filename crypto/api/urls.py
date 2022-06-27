from django.urls import path
from . import views

urlpatterns = [
    path('overview', views.getRoutes, name='api-overview'),
    path('coin', views.GetCoinView.as_view(), name='coin'),
    path('coin/<str:pk>', views.PutCoinView.as_view(), name='coin-update'),
    path('coin/record/allrecords', views.GetAllRecordsByDateView.as_view(), name='all-records-by-date'),
    path('coin/record/<str:pk>', views.GetCoinInfoView.as_view(), name='coin-info'),
    path('coin/record/extra/<str:pk>', views.GetCoinDetailsView.as_view(), name='coin-details-info'),
    path('coin/record/range/<str:pk>', views.GetCoinDateRangeView.as_view(), name='coin-date-range')
]
