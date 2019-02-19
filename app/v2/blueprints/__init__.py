from flask import Blueprint


bp = Blueprint('api', __name__, url_prefix='/api/v2')

from app.v2.views.users import *
from app.v2.views.candidates import *
from app.v2.views.offices import *
from app.v2.views.parties import *
from app.v2.views.votes import *
