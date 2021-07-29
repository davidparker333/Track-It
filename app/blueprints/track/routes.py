from app.blueprints.track.models import Package
from . import bp as track
from app import db
from .track_config import Track_Config
import requests
from .models import Package, Event
from app.blueprints.auth.models import User
from .forms import PackageForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import desc

@track.route('/')
@login_required
def index():
    title = "home"
    packages = Package.query.filter(Package.customer_id == current_user.id).all()
    events = []
    emojis = []
    for package in packages:
        event = Event.query.filter(Event.package_id == package.id).order_by(desc('occured_at')).first()
        events.append(event)
        if event.description == 'Delivered':
            emojis.append('📦🎉')
        elif "delivery" in event.description:
            emojis.append('🚚')
        elif "facility" in event.description:
            emojis.append('🏭')
        else:
            emojis.append('📦💨')
    return render_template('trackHome.html', packages=packages, title=title, events=events, emojis=emojis)

@track.route('/add', methods=['GET', 'POST'])
@login_required
def add_package():
    title = "add"
    form = PackageForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(current_user.id)
        carrier = form.carrier.data
        tracking_number = form.tracking_number.data
        nickname = form.nickname.data
        response = requests.get(Track_Config.base + f'carrier_code={Track_Config.carrier_codes[carrier]}&tracking_number={tracking_number}', headers=Track_Config.headers)
        if tracking_number.isalpha() or response.json()['status_code'] == "UN":
            flash("Unknown tracking number entered. Please check and try again.", "danger")
            return redirect(url_for('track.add_package'))
        elif Package.query.filter(Package.tracking_number == tracking_number).filter(Package.customer_id == user.id).first():
            flash("You're already tracking that package!", "warning")
            return redirect(url_for('track.add_package'))
        else:
            package = Package(user.id, tracking_number, carrier, nickname)
            # Add and commit the package first so it can get an ID
            db.session.add(package)
            db.session.commit()
            # Populate the additional fields and create all Event objects (now tied to that ID)
            package.populate()
            db.session.commit()
            flash('Package added successfully!', 'success')
            return redirect(url_for('track.index'))
    return render_template('addPackage.html', form=form, title=title)