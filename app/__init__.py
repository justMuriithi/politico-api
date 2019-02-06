'''Creating app'''
import os
from flask import Flask
from instance.config import app_config
from .version1 import routes
"""importing the configurations from the .config file which is in the instance folder"""

def create_app(config_name):
    '''creating  the app using the configurations in the dictionary created in the .config file'''
  
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv("SECRET")

    app.register_blueprint(routes.bp)

    return app