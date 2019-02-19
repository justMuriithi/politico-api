from flask import request
from app.version1.util.validate import response
from app.version1.models.offices_model import Office
from app.version1.blueprints import o_bp


offices = Office.offices


@o_bp.route('/offices', methods=['POST', 'GET'])
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
        return response("Your political office was created successfully",
                        201, [office.as_json()])

    elif request.method == 'GET':
        """ Get all offices end point """

        return response('Request was successful', 200, offices)


@o_bp.route('/offices/<int:id>', methods=['GET', 'DELETE'])
def get_office(id):

    model = Office()
    data = model.find_by_id(id)

    if not data:
        return response('Office not found', 404)

    if request.method == 'GET':
        return response('Request was successful', 200, [data])
    else:
        office = model.from_json(data)
        office.delete()
        return response(
            '{} deleted successfully'.format(office.name), 200, [data])
