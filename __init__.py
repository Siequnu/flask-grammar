from flask import Blueprint

bp = Blueprint('grammar', __name__, template_folder = 'templates')

from . import routes, forms, models