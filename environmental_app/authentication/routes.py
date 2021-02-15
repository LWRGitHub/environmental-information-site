from environmental_app import app, db_sql, bcrypt, login
from environmental_app.models import User
from environmental_app.authentication.forms import Signup, Login
from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user

authentication = Blueprint("authentication", __name__)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@authentication.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = Signup()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username = form.username.data,
            password = hashed_password
        )
        db_sql.session.add(user)
        db_sql.session.commit()

        flash('Account created!')
        return redirect(url_for('authentication.login'))
    return render_template('signup.html', form = form)

@authentication.route('/login', methods = ['GET', 'POST'])
def login():
    form = Login()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('homepage'))

    return render_template('login.html', form = form)

@authentication.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homepage'))