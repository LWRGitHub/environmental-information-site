from wtforms.fields.simple import TextAreaField
from environmental_app.models import User, Kickstarter
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.core import FloatField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from wtforms.widgets.core import Select

class KickstarterForm(FlaskForm):

    title = StringField("Title", validators=[
                        DataRequired(), Length(min=3, max=80)])
    photo_url = StringField("Photo Url", validators=[URL(), DataRequired()])
    video_url = StringField("Video Url", validators=[URL(), DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    money_goal = FloatField("Fundraising Goal", validators=DataRequired())
    description = TextAreaField("Description", validators=[DataRequired(),Length(min=3, max=10000)])
    submit = SubmitField("Submit")
