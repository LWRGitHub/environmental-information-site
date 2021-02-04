from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
from yelpapi import YelpAPI
import os
import requests

# This is for the kickstar
from bson.objectid import ObjectId
import jinja2
from pprint import PrettyPrinter
from random import randint

load_dotenv()
mongodb_username = os.getenv('mongodb_username')
mongodb_password = os.getenv('mongodb_password')
mongodb_name = 'kickstarter'
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = MongoClient(f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster0.uzxh5.mongodb.net/{mongodb_name}?retryWrites=true&w=majority")
db = client[mongodb_name]

@app.route('/')
def homepage():
    return "Hello, world!"



''' The code for the kickstarter routes + database is below '''
@app.route('/kickstarter')
def kick_list():
    """Displays the list of startups"""

    startup_data = db.startups.find({})

    context = {
        'startups' : startup_data
    }
    return render_template('startup_list.html', **context)


@app.route('/create_startup', methods=['GET', 'POST'])
def create_rest():
    if request.method == 'POST':

        new_startup = {
            'name': request.form.get('startup_name'),
            'type': request.form.get('type')
        }

        insert_result = db.startups.insert_one(new_startup)

        return redirect(url_for('details', startup_id=insert_result.inserted_id))
    else:
        return render_template('create_startup.html')

@app.route('/search_store', methods=['GET', 'POST'])
def search_store():
    ''' Search for local stores '''
    if request.method == 'POST':
        location = ''
        #checks if ip address is being forwarded. depends if running locally or deployed
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            response = requests.get("http://ip-api.com/json")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']

        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']
            response = requests.get(f"http://ip-api.com/json/{ip}")
            js = response.json()

            city = js['city']
            lat = js['lat']
            lng = js['lon']
    
        store_name = request.form.get('store_name')
        search_results = yelp_api.search_query(term = store_name, latitude = lat, longitude = lng, categories = "vegan")
        business_info = search_results['businesses']

        return render_template('display_store.html', business_info = business_info)

    else:
        return render_template('search_store.html')



if __name__ == '__main__':
    app.run(debug=True)
