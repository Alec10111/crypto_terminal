from django.urls import path
from . import views

"""
Endpoints to add:

"""


urlpatterns = [
    path('apiOverview', views.getRoutes, name='api-overview'),
    path('getCoin', views.GetCoinView.as_view(), name='get-coin'),
    path('getCoin/<str:pk>', views.GetCoinInfoView.as_view(), name='get-coin-info')
]
