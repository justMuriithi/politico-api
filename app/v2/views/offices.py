from flask import Blueprint, request, jsonify, make_response
from app.v2.util.validate import response, exists
from app.v2.models.offices_model import Office
from app.v2.blueprints import bp


@bp.route('/offices', methods=['POST', 'GET'])
def create_office():
    if request.method == 'POST':
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
        return response("Your political office was created successfully", 201, [office.as_json()])

    elif request.method == 'GET':
        """ Get all offices end point """
        model = Office()
        return response('Success', 200, model.load_all())


@bp.route('/offices/<int:id>', methods=['GET', 'DELETE'])
def get_office(id):

    model = Office()
    data = model.find_by('id', id)

    if not data:
        return response('Office not found', 404)

    if request.method == 'GET':
        return response('Request was successful', 200, [data])
    else:
        office = model.from_json(data)
        office.delete(office.id)
        return response(
            '{} deleted successfully'.format(office.name), 200, [data])
