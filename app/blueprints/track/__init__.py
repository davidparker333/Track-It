from flask import Blueprint

bp=Blueprint('track', __name__, url_prefix='/track')

from . import routes, models