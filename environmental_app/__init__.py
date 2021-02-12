from environmental_app.config import Config
from flask import Flask
from flask_googlemaps import GoogleMaps, Map
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from yelpapi import YelpAPI
import os

# This is for the kickstar
from bson.objectid import ObjectId
import jinja2
from pprint import PrettyPrinter
from random import randint

mongodb_username = os.getenv('mongodb_username')
mongodb_password = os.getenv('mongodb_password')
mongodb_name = 'kickstarter'
yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)
google_maps_api_key = os.getenv('google_maps_api_key')

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)

# Initialize flask Google Maps
GoogleMaps(app, key = google_maps_api_key)

# Initialize MongoDB
client = MongoClient(f"mongodb+srv://{mongodb_username}:{mongodb_password}@cluster0.uzxh5.mongodb.net/{mongodb_name}?retryWrites=true&w=majority")
db = client[mongodb_name]

# Blueprints
from environmental_app.routes import main
app.register_blueprint(main)

# with app.app_context():
#     db.create_all()