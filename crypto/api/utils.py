from .models import Coin, CoinHistory
from .serializers import CoinHistorySerializer


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

        registry = CoinHistory.objects.filter(symbol=symbol, date=request.data['date'])

        regSerializer = CoinHistorySerializer(registry, many=True)

        return regSerializer, ''

    elif ('start_date' in request_keys) and ('end_date' in request_keys):
        if request.data['start_date'] == request.data['end_date']:
            return None, 'Dates cannot be equal'
        registry = CoinHistory.objects.filter(
            symbol=symbol,
            date__range=(request.data['start_date'], request.data['end_date'])
        )

        regSerializer = CoinHistorySerializer(registry, many=True)

        return regSerializer, ''

    else:
        return None, 'Something is wrong with your request params.'
