from django.test import TestCase
import json
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import SimpleTestCase
from api.views import *

version = 'v1'


class TestUrls(SimpleTestCase):
    def test_api_overview(self):
        url = reverse('api-overview')
        self.assertEqual(resolve(url).func, getRoutes)

    # def test_getCoin(self):
    #     url = reverse('get-coin')
    #     self.assertEqual(resolve(url).func, getRoutes)

