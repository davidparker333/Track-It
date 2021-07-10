from . import bp as home
from app import db
from flask import render_template, redirect, url_for, flash, request
from app.blueprints.auth.models import User
from app.blueprints.auth.forms import RegisterForm

@home.route('/')
def index():
    title = 'find your stuff'
    return render_template('index.html', title=title)

@home.route('/register', methods=['GET', 'POST'])
def register():
    title = "register"
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter((User.username == username) | (User.email == email)).all()
        if existing_user:
            flash('That username / email is taken. Please sign in or try again', 'danger')
            return redirect(url_for('home.register'))
        new_user = User(username, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Thank you, {username}. You have successfully registered! Please sign in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=title, form=form)