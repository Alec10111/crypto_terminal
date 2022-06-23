import csv
import os
from api.models import Coin, CoinHistory


def run():
    file_list = os.listdir('sample_data/archive')

    Coin.objects.all().delete()
    CoinHistory.objects.all().delete()

    for index, coin_table in enumerate(file_list):
        with open('sample_data/archive/{}'.format(coin_table)) as file:
            read_file = csv.reader(file)
            count = 1
            for record in read_file:
                if count == 1:
                    count += 1
                    pass
                elif count == 2:
                    count += 1
                    Coin.objects.create(name=coin_table[5:-4], symbol=record[2])
                    CoinHistory.objects.create(symbol=record[2], date=record[3], high=record[4], low=record[5],
                                               open=record[6], close=record[7], volume=record[8], marketcap=record[9])

                else:
                    CoinHistory.objects.create(symbol=record[2], date=record[3], high=record[4], low=record[5],
                                               open=record[6], close=record[7], volume=record[8], marketcap=record[9])
