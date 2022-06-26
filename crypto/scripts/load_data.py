import csv
import os
from api.models import Coin, CoinHistory
import pandas as pd
from datetime import datetime


def run(*args):
    file_list = os.listdir('sample_data/archive')

    # Delete all previous records to reset the tables
    if 'replace' in args:
        Coin.objects.all().delete()
        CoinHistory.objects.all().delete()
    for coin_table in file_list:
        print(f'Loading file {coin_table}')
        coin_table_df = pd.read_csv(f'sample_data/archive/{coin_table}')
        coin_table_df.columns = [col.lower() for col in coin_table_df.columns]
        coin_table_df['date'] = coin_table_df['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').date())
        Coin.objects.create(name=coin_table_df.loc[1, 'name'], symbol=coin_table_df.loc[1, 'symbol'])

        for record in coin_table_df.iterrows():
            CoinHistory.objects.create(**record[1].loc['symbol':].to_dict())


"""

    for coin_table in file_list:
        with open('sample_data/archive/{}'.format(coin_table)) as file:
            read_file = csv.reader(file)
            
            count = 1
            for record in read_file:
                if count == 1:  # Skipping the header
                    count += 1
                    pass
                elif count == 2:  # Using first row to create coin table with symbols and names.
                    count += 1
                    Coin.objects.create(name=coin_table[5:-4], symbol=record[2])
                    # We don't pass here
                    CoinHistory.objects.create(symbol=record[2], date=record[3][:10], high=record[4], low=record[5],
                                            open=record[6], close=record[7], volume=record[8], marketcap=record[9])
                else:
                    CoinHistory.objects.create(symbol=record[2], date=record[3][:10], high=record[4], low=record[5],
                                               open=record[6], close=record[7], volume=record[8], marketcap=record[9])
"""
