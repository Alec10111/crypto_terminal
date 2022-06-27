from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Coin, CoinHistory


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class CoinHistorySerializer(ModelSerializer):
    class Meta:
        model = CoinHistory
        fields = '__all__'
