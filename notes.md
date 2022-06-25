# Notes for the technical task
## Data
All necessary data is in `data/archive`.

## Create an interactive tool to answer the following questions
1) What coins are available in our dataset?
2) What was the Close price of X coin at date yyyy-mm-dd (eg: BTC in 2020-01-02)
3) Given a start date and end date, what are the best possible buy and sell times to maximise profit?

## Bonus
- Load the data into SQLite
- Create a REST API backend to serve the data to the tool
- Create a dashboard with useful metrics and graphs

## Tech Stack
- Backend with python django (DRF)
- DB either SQLite or PostgreSQL
- Dashboard with Streamlit?

## Project structure
- Main app crypto, api app

## DB structure
- Coins: coin_id (pk), coin_name, coin_symbol
- Coin_history: coin_id(fk),Date,High,Low,Open,Close,Volume,Marketcap


### Idea 1 (extras)
- Favourites: User_Id, Coin_Faved, Date


