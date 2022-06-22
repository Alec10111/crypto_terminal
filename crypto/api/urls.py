from django.urls import path
from . import views

"""
Endpoints to add:

"""


urlpatterns = [
    path('apiOverview', views.getRoutes, name='api-overview')
]
