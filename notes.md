#Notes for the technical task
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
- API
- DB management
- Data Analysis

## DB structure
- Coin_history (one table for each): Name,Symbol,Date,High,Low,Open,Close,Volume,Marketcap
- Favourites: User_Id, Coin_Faved, Date


## Endpoints
- `/apiOverview` GET "Shows all available endpoints"
- `/getCoin` GET "returns all available coins"
- `/getCoin/<str:pk>` GET "returns info abount single coin"
- `/getCoin/<str:pk>` POST "returns coin data from specified date"
- `/get`


##Progress
IDEA: Dump everything in just one table (is it performant?)

Query to answer question 1(What coins are available in our dataset?)

SELECT DISTINCT Name FROM COIN_TABLE 

