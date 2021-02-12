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

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config.from_object(Config)

client = MongoClient(f"mongodb+srv://{Config.mongodb_username}:{Config.mongodb_username}@cluster0.uzxh5.mongodb.net/{Config.mongodb_name}?retryWrites=true&w=majority")
db = client[mongodb_name]