# Crypto Terminal
Interactive tool to display useful data about cryptocurrencies.

Backed done with Django (Django-rest-framework) and PostgreSQL as database.

The dashboard on the frontend is done with Streamlit, with altair for the line charts.

## Pre-requisites
You need to have python and postgreSQL installed in your machine
## Setup
First you have to either clone the gitbub repo
```console
git clone https://github.com/Alec10111/crypto_terminal
```
Or if you have the source .zip file, just unzip it.
Cd into the project directory
```console
cd crypto_terminal
```
Now you have to install the necessary dependencies to run the project. If you have a different python installation, maybe you have to do python3 and pip3 instead.
```console
pip install -r requirements.txt
```
## Run
To run the project we have to spin up the backend and the frontend.
```console
cd crypto
python manage.py runserver
```
That will start the django server on port 8000. Now we navigate to the streamlit folder and run the application
```console
cd ..
cd streamlit
streamlit run main.py
```
which will run the streamlit app in port 8501.
Enjoy!