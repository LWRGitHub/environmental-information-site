from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("sqlalchemy_database_uri")
    SQLALCHEMY_TRACK_MODIFICATIONS = False