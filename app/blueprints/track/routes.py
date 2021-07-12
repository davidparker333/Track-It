from app.blueprints.track.models import Package
from . import bp as track
from app import db
from .models import Package, Event
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

@track.route('/')
@login_required
def index():
    packages = Package.query.filter(Package.customer_id == current_user.id).all()
    return render_template('trackHome.html', packages=packages)