from . import bp as track
from app import db
from flask import render_template, redirect, url_for, flash, request

@track.route('/')
def index():
    return render_template('trackHome.html')