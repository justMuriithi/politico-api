from flask import Blueprint


o_bp = Blueprint('api_v1', __name__, url_prefix='/api/version1')


from app.version1.views.offices import *
from app.version1.views.parties import *
