'''Creating app'''
import os

from flask import Flask, request, jsonify, abort
from instance.config import app_config
"""importing the configurations from the .config file which is in the instance folder"""


def create_app(config_name):
    '''creating  the app using the configurations in the dictionary created in the .config file'''
  
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv("SECRET")

    @app.route('/create_party/', methods=['POST', 'GET'])
    def create_party():
        parties = []
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                response = jsonify(parties)
                response.status_code = 201
                return response
        else:
            # GET
            parties = []

            for party in parties:
                obj = {
                    'id': party.id,
                    'name': party.name,
                    'date_created': party.date_created,
                    'date_modified': party.date_modified
                }
                parties.append(obj)
            response = jsonify(parties)
            response.status_code = 200
            return response

    return app