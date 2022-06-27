import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import altair as alt
from utils import *

header = st.container()
cInfo_header = st.container()
input_single_coin, specific_date_metrics = st.columns(2)
single_graphics = st.container()
input_compare_coins = st.container()
compare_graphics = st.container()

coins_dict = requests.get('http://localhost:8000/api/coin').json()
coins = [coin['name'] for coin in coins_dict]
stats_list = ['High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap']

with header:
    st.title('Crypto Terminal')
    st.text('This project is an interactive tool to display useful data about cryptocurrencies.')
    st.text('The first sections displays stats for a given currency and best buy and sell dates.')
    st.text('On the second section you can compare multiple coins over time.')
    st.text('Source code: https://github.com/Alec10111/crypto_terminal')

with cInfo_header:
    st.header('Currency Info')

with input_single_coin:
    selected_coin = st.selectbox('Select a coin', options=coins)
    symbol = get_symbol(coins_dict, selected_coin)
    sel_stat = st.selectbox(
        'Select stat', stats_list, key='sel_stat')
    max_min_date = requests.get('http://localhost:8000/api/coin/record/range/{}'.format(symbol)).json()
    min_date = datetime.strptime(max_min_date['min_date'], '%Y-%m-%d')
    max_date = datetime.strptime(max_min_date['max_date'], '%Y-%m-%d')

    start_end_time = st.slider("Select date range", max_date, min_date, value=(min_date, max_date), format="YYYY-MM-DD")
    if start_end_time[0] == start_end_time[1]:
        st.warning('Dates must be different.')
        st.stop()
with specific_date_metrics:
    select_single_date = st.date_input('Date specific data', min_date, min_date, max_date)
    req_single_date = requests.post(
        'http://localhost:8000/api/coin/record/{0}'.format(symbol), data={
            'date': select_single_date
        }).json()
    if not req_single_date:
        st.write('Record not available for this date.')
    else:
        formatted_single_date_data = {
            k.capitalize(): round(v, 4) for k, v in req_single_date[0].items() if k.capitalize() in stats_list
        }
        st.json(formatted_single_date_data)

with single_graphics:
    st.subheader('Stats over time ( {} )'.format(symbol))

    req_range_date = requests.post(
        'http://localhost:8000/api/coin/record/{0}'.format(symbol), data={
            'start_date': start_end_time[0].date(),
            'end_date': start_end_time[1].date()
        })
    req_extra = requests.post(
        'http://localhost:8000/api/coin/record/extra/{0}'.format(symbol), data={
            "start_date": start_end_time[0].date(),
            "end_date": start_end_time[1].date()
        })

    reduced_df = pd.DataFrame(req_range_date.json())[['date', 'symbol', sel_stat.lower()]]

    selection = alt.selection_interval(bind='scales')
    chart1 = alt.Chart(reduced_df).mark_line().encode(
        x=alt.X('date:T'),
        y=alt.Y(sel_stat.lower()),
        color=alt.Color("symbol:N")
    ).add_selection(
        selection
    )
    st.altair_chart(chart1, use_container_width=True)

    adv_data = req_extra.json()
    st.markdown('- **Best buy date**:  {}'.format(adv_data['buy']))
    st.markdown('- **Best sell date**:  {}'.format(adv_data['sell']))
    st.markdown('- **Profit percentage**: {:.2f}\%'.format(adv_data['profit_percentage']))

with input_compare_coins:
    st.header('Compare Currencies')

    selected_coins = st.multiselect(
        'Select a coin', options=coins, default=['Cardano', 'USD Coin', 'XRP'])
    if not selected_coins:
        st.warning('Please select at least one coin.')
        st.stop()
    sel_stat_mul = st.selectbox(
        'Select stat', stats_list, key='sel_stat_mul')

    symbols = [get_symbol(coins_dict, coin) for coin in selected_coins]
    max_min_date_mul = [requests.get('http://localhost:8000/api/coin/record/range/{}'.format(sym)).json() for sym in symbols]
    min_mul = max([rec['min_date'] for rec in max_min_date_mul])
    max_mul = min([rec['max_date'] for rec in max_min_date_mul])
    min_mul = datetime.strptime(min_mul, '%Y-%m-%d')
    max_mul = datetime.strptime(max_mul, '%Y-%m-%d')

    start_end_time_mul = st.slider("Adjust date range", max_mul, min_mul, value=(min_mul, max_mul),
                                   format="YYYY-MM-DD")

    if start_end_time_mul[0] == start_end_time_mul[1]:
        st.warning('Dates must be different.')
        st.stop()

with compare_graphics:
    mul_req_list = [requests.post(
        'http://localhost:8000/api/coin/record/{0}'.format(sym), data={
            'start_date': start_end_time_mul[0].date(),
            'end_date': start_end_time_mul[1].date()
        }).json() for sym in symbols]

    flattened_list = []
    for xs in mul_req_list:
        for x in xs:
            flattened_list.append(x)

    reduced_df_mul = pd.DataFrame(flattened_list)[['date', 'symbol', sel_stat_mul.lower()]]

    chart2 = alt.Chart(reduced_df_mul).mark_line().encode(
        x=alt.X('date:T'),
        y=alt.Y(sel_stat_mul.lower()),
        color=alt.Color("symbol:N")
    ).properties(title="Comparison Chart").add_selection(
        selection
    )
    st.altair_chart(chart2, use_container_width=True)
