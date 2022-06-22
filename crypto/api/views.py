from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


# from .models import
# from .serializers import

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/getCoin',
            'method': 'GET',
            'body': None,
            'description': 'returns an array with all available coins'
        }
    ]
