from environmental_app import db_sql
from flask_login import UserMixin

class User(UserMixin, db_sql.Model):
    """ User information model """
    id = db_sql.Column(db_sql.Integer, primary_key = True)
    username = db_sql.Column(db_sql.String(80), nullable = False, unique = True)
    password = db_sql.Column(db_sql.String(80), nullable = False)