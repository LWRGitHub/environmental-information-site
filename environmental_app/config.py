from dotenv import load_dotenv
import os

load_dotenv()

class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.getenv("sqlalchemy_database_uri")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost/database1"

    SQLALCHEMY_TRACK_MODIFICATIONS = False