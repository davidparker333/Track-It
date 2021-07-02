from . import bp as home
from app import db
from flask import render_template

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/register')
def register():
    return render_template('register.html')