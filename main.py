from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_googlemaps import GoogleMaps, Map
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
google_maps_api_key = os.getenv('google_maps_api_key')

app = Flask(__name__)
app.secret_key = os.urandom(24)
GoogleMaps(app, key=google_maps_api_key)

client = MongoClient(f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster0.uzxh5.mongodb.net/{mongodb_name}?retryWrites=true&w=majority")
db = client[mongodb_name]

def get_coordinates(API_KEY, address_text):
    ''' google maps api to get coordinates from address '''
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json?address="
        + address_text
        + "&key="
        + API_KEY
    ).json()
    return response["results"][0]["geometry"]["location"]

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
    # initializes an empty list that will store a list of dictionaries that contain the coordinates for the
    # markers parameter of business_map
    coordinates_list = []

    if request.method == 'POST':
        location = ''
        # obtains the user's current ip address
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

        # yelp api that provides a list of stores with the category vegan near the user's current latitude/longitude
        search_results = yelp_api.search_query(term = store_name, latitude = lat, longitude = lng, categories = "vegan")
        business_info = search_results['businesses']
        
        # stores pin image and all lat/lng of queried stores into a dictionary to be passed into the map and displayed on the page
        for coordinate in business_info:
            coordinates_dict = {}
            coordinates_dict['icon'] = "/static/images/leaf_pin.png"
            coordinates_dict['lat'] = coordinate['coordinates']['latitude']
            coordinates_dict['lng'] = coordinate['coordinates']['longitude']

            # appends dictionary entry into the list
            coordinates_list.append(coordinates_dict)

        # defines the parameters of the map that will be displayed on the web page
        business_map = Map(
            identifier = "test-map",
            style = "height:700px;width:700px;margin:0;",
            lat = lat,
            lng = lng,
            markers = coordinates_list
        )

        return render_template('display_store.html', business_info = business_info, business_map = business_map)

    else:
        return render_template('search_store.html')



if __name__ == '__main__':
    app.run(debug=True)
