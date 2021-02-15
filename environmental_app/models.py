from environmental_app import db_sql
from sqlalchemy_utils import URLType
from flask_login import UserMixin

class User(UserMixin, db_sql.Model):
    """ User information model """
    id = db_sql.Column(db_sql.Integer, primary_key = True)
    username = db_sql.Column(db_sql.String(80), nullable = False, unique = True)
    password = db_sql.Column(db_sql.String(80), nullable = False)

class Kickstarter(db_sql.Model):
    """ Kickstarter Startup Model"""
    id = db_sql.Column(db_sql.Integer, primary_key=True)
    title = db_sql.Column(db_sql.String(80), nullable=False)
    photo_url = db_sql.Column(URLType)
    video_url = db_sql.Column(URLType)
    created_by_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('user.id'))
    created_by = db_sql.relationship('User')
    end_date = db_sql.Column(db_sql.Date(), nullable=False)
    money_goal = db_sql.Column(db_sql.Float(precision=2), nullable=False)
    description = db_sql.Column(db_sql.String(), nullable=False)
