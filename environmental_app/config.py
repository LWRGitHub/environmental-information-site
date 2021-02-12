from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    mongodb_username = os.getenv('mongodb_username')
    mongodb_password = os.getenv('mongodb_password')
    mongodb_name = 'kickstarter'
    yelp_api = YelpAPI(os.getenv('yelp_api_key'), timeout_s = 3.0)
    google_maps_api_key = os.getenv('google_maps_api_key')