from werkzeug.security import check_password_hash
from . import bp as auth
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from .models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = "login"
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username).first()
        if user is None or not check_password_hash(user.password, password):
            flash("Incorrect Username / Password. Please try again", 'danger')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        flash("You have successfully logged in!", 'success')
        return redirect(url_for('track.index'))
    return render_template('login.html', title=title, form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('You have successfully been logged out', 'warning')
    return redirect(url_for('home.index'))