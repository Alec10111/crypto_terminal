from django.test import TestCase, Client, TransactionTestCase
from django.urls import reverse
from api.models import *


class TestViews(TransactionTestCase):
    def setUp(self):
        self.client = Client()
        self.api_overview = reverse('api-overview')
        self.get_coin = reverse('coin')
        self.post_coin_extra = reverse('coin-details-info', kwargs={'pk': 'BTC'})

    def test_api_overview_GET(self):
        response = self.client.get(self.api_overview)

        self.assertEqual(response.status_code, 200)

    def test_coin_GET(self):
        response = self.client.get(self.get_coin)

        self.assertEqual(response.status_code, 200)

    def test_coin_POST(self):
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
