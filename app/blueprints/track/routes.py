from app.blueprints.track.models import Package
from . import bp as track
from app import db
import os
import requests
from .models import Package, Event
from app.blueprints.auth.models import User
from .forms import PackageForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

key = os.environ.get('SHIPENGINE_API')
base = 'https://api.shipengine.com/v1/tracking?'
headers = {"Host": "api.shipengine.com", "API-Key": key}
carrier_codes = {
    "FedEx": "fedex",
    "USPS": "usps",
    "UPS": "ups"
}

@track.route('/')
@login_required
def index():
    packages = Package.query.filter(Package.customer_id == current_user.id).all()
    return render_template('trackHome.html', packages=packages)

@track.route('/add', methods=['GET', 'POST'])
@login_required
def add_package():
    form = PackageForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.get(current_user.id)
        carrier = form.carrier.data
        tracking_number = form.tracking_number.data
        response = requests.get(base + f'carrier_code={carrier_codes[carrier]}&tracking_number={tracking_number}', headers=headers)
        if tracking_number.isalpha() or response.json()['status_code'] == "UN":
            flash("Unknown tracking number entered. Please check and try again.", "danger")
            return redirect(url_for('track.add_package'))
        else:
            package = Package(user.id, tracking_number, carrier)
            db.session.add(package)
            db.session.commit()
            flash('Package added successfully!', 'success')
            return redirect(url_for('track.index'))
    return render_template('addPackage.html', form=form)