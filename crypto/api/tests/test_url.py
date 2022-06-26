from django.urls import reverse, resolve
from django.test import SimpleTestCase
from api.views import *


class TestUrls(SimpleTestCase):
    def test_api_overview(self):
        url = reverse('api-overview')
        self.assertEqual(resolve(url).func, getRoutes)

    def test_coin(self):
        url = reverse('coin')
        self.assertEqual(resolve(url).func.view_class, GetCoinView)

    def test_coin_allrecords(self):
        url = reverse('all-records-by-date')
        self.assertEqual(resolve(url).func.view_class, GetAllRecordsByDateView)

    def test_coin_pk(self):
        url = reverse('coin-info', kwargs={'pk': 'BTC'})
        self.assertEqual(resolve(url).func.view_class, GetCoinInfoView)

    def test_coin_extra(self):
        url = reverse('coin-details-info', kwargs={'pk': 'BTC'})
        self.assertEqual(resolve(url).func.view_class, GetCoinDetailsView)
