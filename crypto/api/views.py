from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Coin, CoinHistory
from .serializers import CoinSerializer, GroupSerializer, UserSerializer, CoinHistorySerializer
from rest_framework import status
from .utils import maxProfit, date_validations
from django.db.models import Max, Min


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


# Returns a list of available endpoints
class GetCoinOverview(APIView):
    def get(self, request):
        routes = [
            {
                'Endpoint': 'api/overview',
                'method': 'GET',
                'body': None,
                'description': 'returns an array with all available endpoints'
            },
            {
                'Endpoint': 'api/coin',
                'method': 'GET',
                'body': None,
                'description': 'returns an array with all available coins'
            },
            {
                'Endpoint': 'api/coin',
                'method': 'POST',
                'body': {
                    'symbol': 'NC',
                    'name': 'Newcoin'
                },
                'description': 'adds new coin to the database'
            },
            {
                'Endpoint': 'api/coin/<pk>',
                'method': 'PUT',
                'body': {
                    'symbol': 'UBTC',
                    'name': 'UpdatedBitcoin'
                },
                'description': 'updates a coin name and symbol in the database'
            },
            {
                'Endpoint': 'api/coin',
                'method': 'DELETE',
                'body': {
                    'symbol': 'NC',
                    'name': 'Newcoin'
                },
                'description': 'deletes coin from the database'
            },
            {
                'Endpoint': 'api/coin/record/<pk>',
                'method': 'GET',
                'body': None,
                'description': 'returns latest information about the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/<pk>',
                'method': 'POST',
                'body': {
                    'startDate': '2022-03-03',
                    'endDate': '2022-04-03'
                },
                'description': 'returns records within given dates about the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/<pk>',
                'method': 'POST',
                'body': {
                    'date': '2022-03-03'
                },
                'description': 'returns records for given date about the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/<pk>',
                'method': 'PUT',
                'body': {
                    "date": "2019-01-10",
                    "high": 2.9847077975,
                    "low": 2.3791120974,
                    "open": 2.91424758223,
                    "close": 2.4361243181,
                    "volume": 1205353503.11214,
                    "marketcap": 2207725769.14475
                },
                'description': 'updates record on the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/<pk>',
                'method': 'DELETE',
                'body': {
                    "date": "2019-01-10",
                },
                'description': 'deletes record on the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/extra/<pk>',
                'method': 'POST',
                'body': {
                    "startDate": "2018-11-11",
                    "endDate": "2018-11-23"
                },
                'description': 'returns best buy-sell dates and profit percentage on the coin with symbol=pk'
            },
            {
                'Endpoint': 'api/coin/record/allrecords',
                'method': 'POST',
                'body': {
                    'coins': ['ADA', 'BTC'],
                    'startDate': '2022-03-03',
                    'endDate': '2022-04-03'
                },
                'description': 'returns records on given date range for provided coins. If coins parameter is not '
                               'present, it returns all available records on that range. '
            },
            {
                'Endpoint': 'coin/record/range/<pk>',
                'method': 'GET',
                'body': None,
                'description': 'Returns maximum and minimum date available for the given coin.'
            }

        ]
        return Response(routes)


class GetCoinView(APIView):
    # Returns a list of available coins
    def get(self, request):
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)

    # Creates a new coin on the coin table
    def post(self, request):
        Coin.objects.create(**request.data)
        symbol = request.data['symbol']
        created_coin = Coin.objects.get(symbol=symbol)
        created_coin_serializer = CoinSerializer(created_coin, many=False)
        return Response(created_coin_serializer.data, status=status.HTTP_201_CREATED)

    # Deletes coin and all records for that coin.
    def delete(self, request):
        symbol = request.data['symbol']
        coin = Coin.objects.get(symbol=symbol)
        if not coin.exists():
            return Response('Coin not found', status=status.HTTP_404_NOT_FOUND)
        coin_registry = CoinHistory.objects.filter(symbol=symbol)
        number_of_records = len(coin_registry)
        res = {
            'coin': symbol,
            'deleted': '{} records'.format(number_of_records)
        }
        coin_registry.delete()
        coin.delete()
        return Response(res)


class PutCoinView(APIView):
    # Updates a coin in the table
    def put(self, request, pk):
        data = request.data
        existing_coin = Coin.objects.filter(symbol=pk)
        if not existing_coin.exists():
            return Response('Coin not found', status=status.HTTP_404_NOT_FOUND)
        existing_coin.update(**data)
        return Response('Coin updated', status=status.HTTP_204_NO_CONTENT)


class GetCoinInfoView(APIView):
    # Returns last record available for that coin
    def get(self, request, pk):
        max_date_record = CoinHistory.objects.filter(symbol=pk).aggregate(Max('date'))
        max_obj = CoinHistory.objects.get(symbol=pk, date=max_date_record['date__max'])
        max_serializer = CoinHistorySerializer(max_obj, many=False)
        return Response(max_serializer.data)

    # Returns single record for the date, or the date range
    def post(self, request, pk):
        serializer, error = date_validations(request, pk)
        if serializer is None:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    # Updates or Creates a record
    def put(self, request, pk):
        data = request.data
        existing_record = CoinHistory.objects.filter(symbol=request.data['symbol'], date=request.data['date'])
        if not existing_record.exists():
            coin = CoinHistory.objects.create(**data)
            return Response('Record created', status=status.HTTP_201_CREATED)
        else:
            existing_record.update(**data)
            return Response('Record updated', status=status.HTTP_204_NO_CONTENT)

    # Deletes record.
    def delete(self, request, pk):
        record = CoinHistory.objects.filter(symbol=pk, date=request.data['date'])
        if not record:
            return Response('Record not found', status=status.HTTP_404_NOT_FOUND)

        record.delete()
        return Response(request.data)


# More specialized information about the coin in given date

class GetCoinDetailsView(APIView):
    def post(self, request, pk):
        serializer, error = date_validations(request, pk)
        if serializer is None:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        buy, sell = maxProfit(serializer.data)
        analyzed_data = {
            'coin': pk,
            'buy': buy['date'],
            'sell': sell['date'],
            'profit_percentage': sell['high'] * 100 / buy['high'] - 100
        }
        return Response(analyzed_data)


class GetAllRecordsByDateView(APIView):
    def post(self, request):

        start_date = request.data['start_date']
        end_date = request.data['end_date']

        if start_date == end_date:
            return Response('Dates should be different', status=status.HTTP_400_BAD_REQUEST)

        # Get all records in given range
        records = CoinHistory.objects.filter(
            date__range=(start_date, end_date)
        )
        # If coins param provided, get only those coins
        if 'coins' in request.data.keys():
            records = records.filter(
                symbol__in=request.data['coins']
            )
        records_serializer = CoinHistorySerializer(records, many=True)
        return Response(records_serializer.data)


class GetCoinDateRangeView(APIView):
    def get(self, request, pk):
        max_date_record = CoinHistory.objects.filter(symbol=pk).aggregate(Max('date'))
        min_date_record = CoinHistory.objects.filter(symbol=pk).aggregate(Min('date'))

        max_obj = CoinHistory.objects.get(symbol=pk, date=max_date_record['date__max'])
        min_obj = CoinHistory.objects.get(symbol=pk, date=min_date_record['date__min'])

        max_serializer = CoinHistorySerializer(max_obj, many=False)
        min_serializer = CoinHistorySerializer(min_obj, many=False)

        return Response({
            'min_date': min_serializer.data['date'],
            'max_date': max_serializer.data['date']
        })
