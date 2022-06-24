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
from django.db.models import Max
from rest_framework import status
from .utils import maxProfit


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
# Returns a list of available endpoints
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/coin',
            'method': 'GET',
            'body': None,
            'description': 'returns an array with all available coins'
        },
        {
            'Endpoint': '/coin',
            'method': 'PUT',
            'body': {
                "id": 13241,
                "symbol": "BTC",
                "date": "2017-10-02 23:59:59",
                "high": 4470.22998046875,
                "low": 4377.4599609375,
                "open": 4395.81005859375,
                "close": 4409.31982421875,
                "volume": 1431730048.0,
                "marketcap": 73195646775.8
            },
            'description': 'adds a record to the coinHistory table'
        },
        {
            'Endpoint': '/coin/<str:pk>',
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
    # Returns a list of available coins
    def get(self, request):
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)

    # Creates a new coin on the coin table
    def post(self, request):
        data = request.data
        coin = Coin.objects.create(
            name=data.name,
            symbol=data.symbol
        )

    # Updates a coin in the table (not sure why)
    def put(self, request):
        data = request.data
        coin = Coin.objects.get(name=data.name)
        serializer = CoinSerializer(instance=coin, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Something went wrong with your request.', status=status.HTTP_404_NOT_FOUND)


# TODO:
class GetCoinInfoView(APIView):
    # Idea: Return last record available for that coin
    def get(self, request, pk):
        print(request.data)
        symbol = Coin.objects.get(symbol=pk)
        print(symbol)
        # registry = CoinHistory.objects.filter(symbol=symbol)
        # regSerializer = CoinHistorySerializer(registry, many=True)
        return Response('To do')

    # Returns single record for the date, or the interval
    def post(self, request, pk):
        if 'date' in request.data.keys():
            symbol = Coin.objects.get(symbol=pk)
            print(symbol)
            registry = CoinHistory.objects.filter(symbol=symbol).get(date=request.data['date'])
            regSerializer = CoinHistorySerializer(registry, many=False)
            return Response(regSerializer.data)
        else:
            symbol = Coin.objects.get(symbol=pk)
            print(symbol)
            registry = CoinHistory.objects.filter(
                symbol=symbol,
                date__range=(request.data['startDate'], request.data['endDate'])
            )
            regSerializer = CoinHistorySerializer(registry, many=True)
            return Response(regSerializer.data)

    # Updates a record
    def put(self, request, pk):
        updated_data = request.data
        existing_record = CoinHistory.objects.filter(symbol=request.data['symbol'], date=request.data['date'])
        serializer = CoinHistorySerializer(instance=existing_record, data=updated_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response('Something went wrong with your request.', status=status.HTTP_404_NOT_FOUND)

    # Deletes the coin and the recors. Dont use it
    def delete(self, request, pk):
        pass


# More specialized information about the coin in given date
class GetCoinDetailsView(APIView):
    def post(self, request, pk):
        # symbol = Coin.objects.filter(symbol=pk)
        coins = CoinHistory.objects.filter(
            symbol=pk,
            date__range=(request.data['startDate'], request.data['endDate'])
        )
        prices = [CoinHistorySerializer(x, many=False).data for x in coins]

        buy, sell = maxProfit(prices)
        analyzed_data = {
            'coin': pk,
            'buy': buy['date'],
            'sell': sell['date'],
            'profit_percentage': sell['high'] * 100 / buy['high'] - 100
        }
        return Response(analyzed_data)
