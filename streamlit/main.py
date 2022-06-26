import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import altair as alt
from utils import *




header = st.container()
cInfo_header = st.container()
input_single_coin, specific_date_metrics = st.columns(2)
single_metrics = st.container()
input_compare_coins = st.container()
compare_graphics = st.container()

getCoins = requests.get('http://localhost:8000/api/coin')
coins_dict = getCoins.json()
coins = [coin['name'] for coin in coins_dict]

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
    sel_stat = st.selectbox(
        'Select stat', ('High', 'Low', 'Open', 'Close', 'Volume', 'Marketcap'), key='sel_stat')

    symbol = getSymbol(coins_dict, selected_coin)
    # start_date = st.date_input(
    #     'Insert start date', value=datetime(2018, 5, 17))
    # end_date = st.date_input('Insert end date', value=datetime(2019, 5, 17))
    start_end_time = st.slider("Select date range", value=(
        datetime(2019, 1, 9), datetime(2020, 9, 30)), format="YYYY-MM-DD")

with specific_date_metrics:
    select_single_date = st.date_input('Date specific data', datetime(2019, 1, 1))
    req_single_date = requests.post(
        'http://localhost:8000/api/coin/{0}'.format(symbol), data={
            'date': select_single_date
        }).json()
    formatted_single_date_data = {k: round(v, 4) for k, v in req_single_date.items() if
                                  k in ['high', 'low', 'open', 'close', 'volume', 'marketcap']}
    st.json(formatted_single_date_data)

with single_metrics:
    st.subheader('Stats over time ( {} )'.format(symbol))

    req2 = requests.post(
        'http://localhost:8000/api/coin/{0}'.format(symbol), data={
            'start_date': start_end_time[0],
            'end_date': start_end_time[1]
        })
    reqf = requests.post(
        'http://localhost:8000/api/coin/extra/{0}'.format(symbol), data={
            "start_date": start_end_time[0],
            "end_date": start_end_time[1]
        })
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
    st.markdown('- **Profit percentage**: {:.2f}\%'.format(adv_data['profit_percentage']))

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
        'http://localhost:8000/api/coin/{0}'.format(sym), data={
            'start_date': start_end_time_mul[0],
            'end_date': start_end_time_mul[1]
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
