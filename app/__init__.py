'''Creating app'''
import os
from flask import Flask, jsonify, redirect
from instance.config import app_config
from .v2.blueprints import bp
from .version1.blueprints import o_bp
from .v2.db.database_config import Database
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config_name):
    '''creating the app using the configurations in the .config file'''

    # to allow for heroku devployment
    is_prod = os.environ.get('IS_HEROKU', None)
    if is_prod:
        config_name = 'development'

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    create_db(config_name)

    app.secret_key = os.getenv("SECRET")

    app.register_blueprint(o_bp)
    app.register_blueprint(bp)

    JWTManager(app)
    CORS(app)

    @app.route('/')
    @app.route('/index')
    def index():
        """ The welcome screen of the api """

        return redirect(
                    'https://app.swaggerhub.com/apis/justMuriithi/politico-api_v_2/1.0-oas3')

    @app.errorhandler(404)
    def page_not_found(error):
        """ Handler for error 404 """

        return jsonify({
            'status': 404, 'message': 'The requested resource was not found'
        })

    @app.errorhandler(500)
    def internal_server(error):
        """ Handler for error 500 """

        return jsonify({
            'status': 500, 'message':
            'Unable to process your request at this time'
        })

    @app.errorhandler(405)
    def method_not_allowed(error):
        """ Handler for error 405 """

        return jsonify({'status': 405, 'message': 'Method not allowed'})

    @app.errorhandler(400)
    def bad_request(error):
        """ Handler for error 400 """

        return jsonify({'status': 400, 'message': 'Please review \
            your request and try again'})

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
