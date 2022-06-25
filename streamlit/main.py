import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def getSymbol(cList, coin):
    filtered = list(filter(lambda x: x['name'] == coin, cList))
    dicte = filtered[0]
    return dicte['symbol']


def flatten(xss):
    return [x for xs in xss for x in xs]


header = st.container()
input_single_coin = st.container()
single_metrics = st.container()
input_compare_coins = st.container()
compare_graphics = st.container()

getCoins = requests.get('http://localhost:8000/v1/coin')
coins_dict = getCoins.json()
coins = [coin['name'] for coin in getCoins.json()]

with header:
    st.title('Crypto Terminal')
    st.text('This project is an interactive tool to display useful data about cryptocurrencies.')
    st.text('The first sections displays stats for a given currency and best buy and sell dates.')
    st.text('The second section you can compare multiple coins over time.')
    st.text('Source code: https://github.com/Alec10111/crypto_terminal')

with input_single_coin:
    st.header('Currency Info')

    selected_coin = st.selectbox('Select a coin', options=coins)
    sel_stat = st.selectbox(
        'Select stat', ('High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap'), key='sel_stat')

    symbol = getSymbol(coins_dict, selected_coin)
    # start_date = st.date_input(
    #     'Insert start date', value=datetime(2018, 5, 17))
    # end_date = st.date_input('Insert end date', value=datetime(2019, 5, 17))
    start_end_time = st.slider("Select date range", value=(
        datetime(2019, 1, 9), datetime(2020, 9, 30)), format="YYYY-MM-DD")


with single_metrics:
    st.subheader('Stats over time ( {} )'.format(symbol))

    req2 = requests.post(
        'http://localhost:8000/v1/coin/{0}'.format(symbol), data={
            'startDate': start_end_time[0],
            'endDate': start_end_time[1]
        })
    reqf = requests.post('http://localhost:8000/v1/coin/extra/{0}'.format(
        symbol), data={"startDate": start_end_time[0], "endDate": start_end_time[1]})
    # chart_data = pd.DataFrame(
    #     {
    #         'Date': [record['date'] for record in req2.json()],
    #         sel_stat: [record[sel_stat] for record in req2.json()]

    #     }
    # )
    # chart_data = chart_data.set_index('Date')
    chart_data = pd.DataFrame(req2.json())
    display_df = chart_data[['date', 'high', 'low',
                             'open', 'close', 'volume', 'marketcap']]
    reduced_df = chart_data[['date', 'symbol', sel_stat.lower()]]
    # reduced_df = reduced_df.set_index('date')
    # st.dataframe(reduced_df)

    selection = alt.selection_interval(bind='scales')
    selection2 = alt.selection_multi(fields=[sel_stat.lower()])
    chart1 = alt.Chart(reduced_df).mark_line().encode(
        x=alt.X('date:T'),
        y=alt.Y(sel_stat.lower()),
        color=alt.Color("symbol:N")
    ).add_selection(
        selection, selection2
    )
    st.altair_chart(chart1, use_container_width=True)

    # st.line_chart(reduced_df, use_container_width=True)

    adv_data = reqf.json()
    st.markdown('- **Best buy date**:  {}'.format(adv_data['buy']))
    st.markdown('- **Best sell date**:  {}'.format(adv_data['sell']))
    st.markdown(
        '- **Profit percentage**: {:.2f}\%'.format(adv_data['profit_percentage']))

with input_compare_coins:
    st.header('Compare Currencies')

    selected_coins = st.multiselect(
        'Select a coin', options=coins, default=['Cardano', 'USDCoin', 'XRP'])
    sel_stat_mul = st.selectbox(
        'Select stat', ('High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap'), key='sel_stat_mul')

    symbols = [getSymbol(coins_dict, coin) for coin in selected_coins]
    # start_date = st.date_input(
    #     'Insert start date', value=datetime(2018, 5, 17))
    # end_date = st.date_input('Insert end date', value=datetime(2019, 5, 17))
    start_end_time_mul = st.slider("Adjust date range", value=(
        datetime(2019, 1, 19), datetime(2020, 9, 30)), format="YYYY-MM-DD")

with compare_graphics:
    mul_req_list = [requests.post(
        'http://localhost:8000/v1/coin/{0}'.format(sym), data={
            'startDate': start_end_time_mul[0],
            'endDate': start_end_time_mul[1]
        }).json() for sym in symbols]

    flattened_list = []
    for xs in mul_req_list:
        for x in xs:
            flattened_list.append(x)

    mul_df = pd.DataFrame(flattened_list)
    reduced_df_mul = mul_df[['date', 'symbol', sel_stat_mul.lower()]]
    # reduced_df_mul = reduced_df_mul.set_index('date')
    # st.dataframe(reduced_df_mul)

    chart2 = alt.Chart(reduced_df_mul).mark_line().encode(
        x=alt.X('date:T'),
        y=alt.Y(sel_stat_mul.lower()),
        color=alt.Color("symbol:N")
    ).properties(title="Comparison Chart").add_selection(
        selection
    )
    st.altair_chart(chart2, use_container_width=True)
