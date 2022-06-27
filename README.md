# Crypto Terminal
Interactive tool to display useful data about cryptocurrencies.

Backend done with Django (Django-rest-framework) and PostgreSQL as database.

The dashboard on the frontend is done with Streamlit.

## Pre-requisites
You need to have python, postgresql and a postgresql client installed on your machine. Mine is Python 3.9.9 and Postgresql 14.3 

## Setup
First you have to either clone the gitbub repo
```console
git clone https://github.com/Alec10111/crypto_terminal
```
or if you have the source .zip file, unzip it.

Cd into the project directory
```console
cd crypto_terminal
```
Now create a virtual environment (There are various ways to do this: conda, venv, etc)
```console
python -m venv env
source env/bin/activate
```
After that, you have to install the necessary dependencies to run the project.
```console
pip install -r requirements.txt
```
**Note:** If an error rises when installing psycopg2, you can manually install the binary with
```console
pip install psycopg2-binary
```
### DB setup
In order to set up the database we need to update the `settings.py` file
```console
cd crypto/crypto
```
Now on the file we look for the database settings, which will be a dictionary like this:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crypto-db',
        'USER': 'alec',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
You have to start a connection on the postgresql client.
Now update User, Password, Host and Port on `settings.py` to match the postgresql client.
Then you have to create a new database called crypto-db.

After that, we have to run migrations to create the tables on the database. Navigate back to the directoy where `manage.py` is at.
```console
cd ..
python manage.py makemigrations
python manage.py migrate
```
This will create our tables according to the models on the project.
Now to load the sample data we need to run the script `load_data.py`
```console
python manage.py runscript load_data
```
If we want to re-load the data and replace the existing records, we can add the argument 'replace'
```
 python manage.py runscript load_data --script-args replace
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