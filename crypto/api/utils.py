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
from rest_framework import status


def maxProfit(prices):
    buy = 0
    sell = 1
    max_profit = 0
    for i in range(1, len(prices)):

        # Checking for lower buy value
        if prices[buy]['high'] > prices[i]['high']:
            buy = i

        # Checking for higher profit
        elif prices[i]['high'] - prices[buy]['high'] > max_profit:
            sell = i
            max_profit = prices[i]['high'] - prices[buy]['high']

    return prices[buy], prices[sell]


def date_validations(request, pk):
    request_keys = request.data.keys()
    symbol = Coin.objects.get(symbol=pk)

    if 'date' in request_keys:

        registry = CoinHistory.objects.filter(symbol=symbol).get(date=request.data['date'])

        regSerializer = CoinHistorySerializer(registry, many=False)

        return regSerializer, ''

    elif ('start_date' in request_keys) and ('end_date' in request_keys):

        registry = CoinHistory.objects.filter(
            symbol=symbol,
            date__range=(request.data['start_date'], request.data['end_date'])
        )

        regSerializer = CoinHistorySerializer(registry, many=True)

        return regSerializer, ''

    else:
        return None, 'Something is wrong with your request params.'
