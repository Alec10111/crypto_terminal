from django.test import TestCase, Client
from django.urls import reverse
from .test_data import base_data
from api.models import Coin, CoinHistory
from api.serializers import CoinHistorySerializer

class TestViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        base_data(cls)

    def setUp(self):
        # Coin.objects.bulk_create([Coin(**data) for data in test_coins])
        # CoinHistory.objects.create(**json_data)
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
        self.assertIn({
            "id": 1,
            "name": "Bitcoin",
            "symbol": "BTC"
        }, response.data)

    def test_get_coin_record_date_POST(self):
        response = self.client.post(self.post_coin, {
            "date": "2018-11-13"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn({
            "id": 1,
            "symbol": "BTC",
            "date": "2018-11-13",
            "high": 6423.25,
            "low": 6350.17,
            "open": 6413.63,
            "close": 6411.27,
            "volume": 3939060000.0,
            "marketcap": 111373453740.24
        }, response.data)

    def test_get_coin_records__date_range_POST(self):
        response = self.client.post(self.post_coin, {
            "start_date": "2018-11-11",
            "end_date": "2018-11-15"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn({
            "id": 1,
            "symbol": "BTC",
            "date": "2018-11-13",
            "high": 6423.25,
            "low": 6350.17,
            "open": 6413.63,
            "close": 6411.27,
            "volume": 3939060000.0,
            "marketcap": 111373453740.24
        }, response.data)

    def test_create_record_PUT(self):
        response = self.client.put(self.post_coin, {
            "symbol": "ETH",
            "date": "2018-11-11",
            "high": 212.999,
            "low": 208.868,
            "open": 212.479,
            "close": 211.34,
            "volume": 1501600000.0,
            "marketcap": 21798464880.6961
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_update_record_PUT(self):
        response = self.client.put(self.post_coin, {
            "symbol": "BTC",
            "date": "2018-11-13",
            "high": 123.25,
            "low": 123.17,
            "open": 123.63,
            "close": 123.27,
            "volume": 123.0,
            "marketcap": 123.24
        }, content_type='application/json')
        self.assertEqual(response.status_code, 204)

    def test_delete_record_DELETE(self):
        response = self.client.delete(self.post_coin, {
            "date": "2018-11-13"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_negative_delete_record_DELETE(self):
        response = self.client.delete(self.post_coin, {
            "date": "2030-11-13"
        }, content_type='application/json')
        self.assertEqual(response.status_code, 404)
