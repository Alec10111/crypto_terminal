from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from api.models import Coin, CoinHistory
import json


class TestViews(TransactionTestCase):

    def setUp(self):
        json_data = {
            "symbol": "BTC",
            "date": "2018-11-13",
            "high": 6423.25,
            "low": 6350.17,
            "open": 6413.63,
            "close": 6411.27,
            "volume": 3939060000.0,
            "marketcap": 111373453740.24
        }
        Coin.objects.create(name='Bitcoin', symbol='BTC')
        CoinHistory.objects.create(**json_data)
        self.client = Client()
        self.api_overview = reverse('api-overview')
        self.coin = reverse('coin')
        self.post_coin = reverse('coin-info', kwargs={'pk': 'BTC'})
        self.post_coin_extra = reverse('coin-details-info', kwargs={'pk': 'BTC'})

    def test_api_overview_GET(self):
        response = self.client.get(self.api_overview)

        self.assertEqual(response.status_code, 200)

    def test_coin_GET(self):
        response = self.client.get(self.coin)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{
            "id": 2,
            "name": "Bitcoin",
            "symbol": "BTC"
        }])

    def test_get_coin__record_POST(self):
        response = self.client.post(self.post_coin, {
            "start_date": "2018-11-11",
            "end_date": "2018-11-15"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn({
            "symbol": "BTC",
            "date": "2018-11-13",
            "high": 6423.25,
            "low": 6350.17,
            "open": 6413.63,
            "close": 6411.27,
            "volume": 3939060000.0,
            "marketcap": 111373453740.24
        },response.data)


"""

    def teste_coin_POST(self):
        response = self.client.post(self.post_coin_extra, {
            "startDate": "2018-11-11",
            "endDate": "2019-11-23"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, {
            "coin": 'BTC',
            "buy": "2019-02-07",
            "sell": "2019-08-28",
            "profit_percentage": 2159982105.5081215
        })
"""
