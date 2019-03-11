from flask import request, abort, make_response, jsonify, current_app
from app.v2.util.validate import response, response_error, valid_email
from app.v2.models.user_model import User
from app.v2.blueprints import bp
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_sendgrid import SendGrid


@bp.route('/auth/signup', methods=['POST'])
def register_user():
    """ Register user end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    if request.method == 'POST':
        try:
            first_name = data['firstname']
            last_name = data['lastname']
            national_id = data['national_id']
            email = data['email']
            admin = False
            password = data['password']
        except KeyError as e:
            return response_error("{} field is required"
                                  .format(e.args[0]), 400)

        user = User(first_name, last_name, national_id, email, admin, password)

    if not user.validate_object():
        return response_error(user.error_message, user.error_code)

    if not get_jwt_identity():
        user.admin = False

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

    if not valid_email(email):
        return response_error('Please provide a valid email', 422)

    elif not user:
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


@bp.route('/auth/reset', methods=['POST'])
def reset_password():
    """ Reset user password end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        email = data['email']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    model = User()

    if not valid_email(email):
        return response_error('Please provide a valid email', 422)

    user = model.find_by('email', email)

    if not user:
        return response_error('User not found', 404)

    mail = SendGrid(current_app)

    model = User(id=user['id'])
    model.create_tokens()

    action_url = """
    https://justmuriithi.github.io/politico/user/password-reset.html?token={}
    """.format(model.access_token)

    with open('reset_mail.txt', 'r') as reset_format:
        text = reset_format.read().replace('\n', '')
        text = text.replace('action_url', action_url)
        text = text.replace('username', user['firstname'])

    mail.send_email(
        from_email='admin@politico.com',
        to_email=email,
        subject='Password reset link',
        html=text
    )

    response_data = {
        'status': 200,
        'data': [
            {
                "message": "Check your email for password reset link",
                "email": email
            }
        ]
    }

    return make_response(jsonify(response_data), 200)


@bp.route('/reset-password', methods=['POST'])
@jwt_required
def change_password():
    """ Change user password end point """

    data = request.get_json()

    if not data:
        return response_error("No data was provided", 400)

    try:
        new_password = data['password']
    except KeyError as e:
        return response_error("{} field is required".format(e.args[0]), 400)

    if len(new_password) < 6:
        abort(
            response_error("Password must be at least 6 characters long", 422))

    model = User()

    user = model.find_by('id', get_jwt_identity())

    if not user:
        abort(
            response_error(
                "We could not find your account. Please sign up", 404))

    model.edit('password', generate_password_hash(new_password), user['id'])

    response_data = {
        'status': 200,
        'data': [
            {
                "message": "Your password has been updated",
            }
        ]
    }

    return make_response(jsonify(response_data), 200)
