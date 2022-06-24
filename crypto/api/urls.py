from django.urls import path
from . import views

"""
Endpoints to add:

"""

urlpatterns = [
    path('apiOverview', views.getRoutes, name='api-overview'),
    path('coin', views.GetCoinView.as_view(), name='coin'),
    path('coin/<str:pk>', views.GetCoinInfoView.as_view(), name='coin-info'),
    path('coin/extra/<str:pk>', views.GetCoinDetailsView.as_view(), name='coin-details-info')
]
