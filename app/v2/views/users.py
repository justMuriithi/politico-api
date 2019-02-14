from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.util.validate import response, exists, response_error
from app.v2.models.user_model import User
from app.v2.blueprints import bp
from werkzeug.security import check_password_hash


@bp.route('/auth/signup', methods=['POST'])
def register_user():
    """ Register user end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        first_name = data['firstname']
        last_name = data['lastname']
        national_id = data['national_id']
        email = data['email']
        is_admin = data['isAdmin']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    user = User(first_name, last_name, national_id, email, is_admin)

    if not user.validate_object():
        return response_error(user.error_message, user.error_code)

    user.save()

    response_data = {
        'token': user.access_token,
        'user': user.as_json()
    }

    # return registered user
    return response("Success", 201, [response_data])


@bp.route('/auth/login', methods=['POST'])
def login():
    """ login user end point """

    message = ""
    status = 200
    response_data = None

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        email = data['email']
        password = data['password']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    user = User().find_by('email', email)

    if not user:
        message = "User not registered"
        status = 404

    elif not check_password_hash(user['password'], password):
        message = "Incorrect password"
        status = 401

    else:
        model = User(id=user['id'])
        model.create_tokens()

        status = 200
        message = 'Success'

        del user['password']

        response_data = {
            'token': model.access_token,
            'user': user
        }

    # return registered user
    if response_data:
        return response(message, status, [response_data])

    return response_error(message, status)
