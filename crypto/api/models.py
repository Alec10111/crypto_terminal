from django.db import models


class Coin(models.Model):
    name = models.TextField(max_length=20)
    symbol = models.CharField(max_length=5, default='')

    def __str__(self):
        return self.symbol


class CoinHistory(models.Model):
    symbol = models.CharField(max_length=5, default=''),
    date = models.TextField(max_length=20)
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    marketcap = models.FloatField()
