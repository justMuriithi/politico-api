from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from app.v2.util.validate import response, exists, response_error
from app.v2.models.user_model import User
from app.v2.blueprints import bp


users = User.users


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

    # return registered user
    return response("Success", 201, [user.as_json()])