from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from environmental_app.models import User

class Signup(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 3, max = 40)])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 3)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class Login(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 3, max = 40)])
    password = PasswordField('Password', validators = [DataRequired(), Length(min = 3)])
    submit = SubmitField('Log In')