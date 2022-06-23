from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Coin, CoinHistory
from .serializers import CoinSerializer, GroupSerializer, UserSerializer, CoinHistorySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/getCoin',
            'method': 'GET',
            'body': None,
            'description': 'returns an array with all available coins'
        },
        {
            'Endpoint': '/getCoin/<str:pk>',
            'method': 'GET',
            'body': None,
            'description': 'returns latest information about the coin'
        },
        {
            'Endpoint': '/getCoin',
            'method': 'POST',
            'body': {
                'coin': 'cardano',
                'startDate': '2022-03-03',
                'endDate': '2022-04-03'
            },
            'description': 'returns best prices to buy and sell within given dates'
        }

    ]
    return JsonResponse(routes, safe=False)


class GetCoinView(APIView):
    def get(self, request):
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)


class GetCoinInfoView(APIView):
    def get(self, request, pk):
        print(request.data)
        symbol = Coin.objects.get(symbol=pk)
        print(symbol)
        # registry = CoinHistory.objects.filter(symbol=symbol)
        # regSerializer = CoinHistorySerializer(registry, many=True)
        return Response("Pending implementation")

    def post(self, request, pk):
        print(request.data)
        symbol = Coin.objects.get(symbol=pk)
        print(symbol)
        registry = CoinHistory.objects.filter(symbol=symbol).get(date=request.data['date'])
        regSerializer = CoinHistorySerializer(registry, many=False)
        return Response(regSerializer.data)
