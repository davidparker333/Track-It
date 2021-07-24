from app import db
from .track_config import Track_Config
import requests
import datetime

class Package(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    customer_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    tracking_number = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    tracking_url = db.Column(db.String(255))
    status = db.Column(db.String(50))
    status_description = db.Column(db.String(255))
    ship_date = db.Column(db.DateTime)
    estimated_delivery_date = db.Column(db.DateTime)
    actual_delivery_date = db.Column(db.DateTime)
    exception_description = db.Column(db.String(255))
    carrier = db.Column(db.String(100), nullable=False)
    events = db.relationship('Event', backref='package', lazy='dynamic')

    def __init__(self, customer_id, tracking_number, carrier):
        self.customer_id = customer_id
        self.tracking_number = tracking_number
        self.carrier = carrier

    def __repr__(self):
        return f'<Package Object | {self.id}>'

    def __str__(self):
        return f'Package - {self.tracking_number} / ID {self.id}'

    def populate(self):
        response = requests.get(Track_Config.base + f'carrier_code={Track_Config.carrier_codes[self.carrier]}&tracking_number={self.tracking_number}', headers=Track_Config.headers).json()
        self.tracking_url = response['tracking_url']
        self.status = response['status_code']
        self.status_description = response['status_description']
        self.ship_date = response['ship_date']
        self.estimated_delivery_date = response['estimated_delivery_date']
        self.actual_delivery_date = response['actual_delivery_date']
        self.exception_description = response['exception_description']
        # There's a problem with this for some reason. Check into this
        # self.events = response['events']


class Event(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    package_id = db.Column(db.Integer(), db.ForeignKey('package.id'), nullable=False)
    occured_at = db.Column(db.DateTime)
    description = db.Column(db.String(255), nullable=False)
    city_locality = db.Column(db.String(100))
    state = db.Column(db.String(30))
    postal_code = db.Column(db.String(10))
    signer = db.Column(db.String(255))

    def __init__(self, package_id, description):
        self.package_id = package_id
        self.description = description

    def __repr__(self):
        return f'<Event Object | {self.id}>'

    def __str__(self):
        return f'Event - {self.description} / ID {self.id} / Package {self.package_id}'