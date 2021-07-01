from . import bp as auth
from app import db
from flask import render_template

@auth.route('/login')
def login():
    return render_template('login.html')