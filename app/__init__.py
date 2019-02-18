'''Creating app'''
import os
from flask import Flask, jsonify
from instance.config import app_config
from .v2.views import offices, parties, users, votes, candidates
from .v2.blueprints import bp
from .version1.blueprints import o_bp
from .v2.db.database_config import Database
from flask_jwt_extended import JWTManager

"""importing the configurations from the .config file which is in the instance folder"""


def create_app(config_name):
    '''creating the app using the configurations in the dictionary created in the .config file'''

    # to allow for heroku devployment
    is_prod = os.environ.get('IS_HEROKU', None)
    if is_prod:
        config_name = 'development'
        os.environ["DATABASE_URL"] = "dbname='politico' host='127.0.0.1' user='voter' password='voter'"

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    create_db(config_name)

    app.secret_key = os.getenv("SECRET")

    app.register_blueprint(bp)

    jwt = JWTManager(app)


    @app.errorhandler(404)
    def page_not_found(error):
        """ Handler for error 404 """

        return jsonify({
            'status': 404, 'message': 'The requested resource was not found'
        })

    @app.errorhandler(405)
    def method_not_allowed(error):
        """ Handler for error 405 """

        return jsonify({'status': 405, 'message': 'Method not allowed'})

    @app.errorhandler(400)
    def bad_request(error):
        """ Handler for error 400 """

        return jsonify({'status': 400, 'message': 'Please review your request and try again'})

    return app

def create_db(config_name):
    """ Create all db tables """

    try:
        db = Database(config_name)
        db.init_connection()
        db.create_db()
        db.create_super_user()

    except Exception as error:
        print('Error creating the database: {}'.format(str(error)))