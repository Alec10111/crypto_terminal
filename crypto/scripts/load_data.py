import csv
import os
from api.models import Coin, CoinHistory
import pandas as pd
from datetime import datetime


def run(*args):
    file_list = os.listdir('sample_data/archive')

    if 'replace' in args:
        Coin.objects.all().delete()
        CoinHistory.objects.all().delete()
    for coin_table in file_list:
        print('Loading file {}'.format(coin_table))
        coin_table_df = pd.read_csv('sample_data/archive/{}'.format(coin_table))
        coin_table_df.columns = [col.lower() for col in coin_table_df.columns]
        coin_table_df['date'] = coin_table_df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        Coin.objects.create(name=coin_table_df.loc[1, 'name'], symbol=coin_table_df.loc[1, 'symbol'])

        for record in coin_table_df.iterrows():
            CoinHistory.objects.create(**record[1].loc['symbol':].to_dict())

