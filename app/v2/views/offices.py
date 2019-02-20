from flask import request
from app.v2.util.validate import response, response_error
from app.v2.models.offices_model import Office
from app.v2.blueprints import bp
from flask_jwt_extended import (jwt_required)
from app.v2.util.jwt_utils import admin_required


@bp.route('/offices', methods=['POST'])
@admin_required
def create_office():
    """ Create office end point """

    data = request.get_json()

    if not data:
        return response("No data was provided", 400)

    try:
        category = data['category']
        name = data['name']
    except KeyError as e:
        return response("{} field is required".format(e.args[0]), 400)

    office = Office(name, category)

    if not office.validate_object():
        return response(office.error_message, office.error_code)

    # append new office to list
    office.save()

    # return added office
    return response("Your political office was created successfully",
                    201, [office.as_json()])


@bp.route('/offices', methods=['GET'])
@jwt_required
def get_offices():
    """ Get all offices end point """
    model = Office()
    return response('Success', 200, model.load_all())


@bp.route('/offices/<int:id>', methods=['GET'])
@jwt_required
def get_office(id):

    model = Office()
    data = model.find_by('id', id)

    if not data:
        return response('Office not found', 404)

    return response('Request was successful', 200, [data])


@bp.route('/offices/<int:office_id>', methods=['DELETE'])
@admin_required
def delete_office(office_id):

    model = Office()
    data = model.find_by('id', office_id)

    if not data:
        return response_error('Office not found', 404)

    office = model.from_json(data)
    office.delete(office.id)
    return response(
        '{} deleted successfully'.format(office.name), 200, [data])
