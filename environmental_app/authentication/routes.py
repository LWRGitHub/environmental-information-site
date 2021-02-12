from environmental_app import app, db_sql, bcrypt
from environmental_app.models import User
from environmental_app.authentication.forms import Signup, Login
from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

authentication = Blueprint("authentication", __name__)

@authentication.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = Signup()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('uft-8')
        user = User(
            username = form.username.data,
            password = hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Account created!')
        return redirect(url_for('authentication.login'))