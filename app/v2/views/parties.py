from flask import request
from app.v2.models.parties_model import Party
from app.v2.util.validate import response, not_admin
from app.v2.blueprints import bp
from flask_jwt_extended import (jwt_required)


@bp.route('/parties', methods=['POST', 'GET'])
@jwt_required
def create_party():
    if request.method == 'POST':
        """ Create party end point """

        restricted = not_admin()
        if restricted:
            return restricted

        data = request.get_json()

        if not data:
            return response("No data was provided", 400)

        try:
            name = data['name']
            hqAddress = data['hqAddress']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        party = Party(name, hqAddress)

        if not party.validate_object():
            return response(party.error_message, party.error_code)

        party.save()

        # return added party
        return response("Your political party was created successfully",
                        201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """
        model = Party()
        return response('Success', 200, model.load_all())


@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
@jwt_required
def get_party(id):

    model = Party()
    data = model.find_by('id', id)

    if not data:
        return response('Party not found', 404)

    if request.method == 'GET':
        return response('Request was successful', 200, [data])
    else:
        restricted = not_admin()
        if restricted:
            return restricted
        party = model.from_json(data)
        party.delete(party.id)
        return response(
            '{} deleted successfully'.format(party.name), 200, [data])


@bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
@jwt_required
def edit_party(id, name):

    restricted = not_admin()
    if restricted:
        return restricted

    model = Party()
    data = model.find_by('id', id)

    if not data:
        return response('Party not found', 404)

    party = model.from_json(data)
    party.name = name

    if not party.validate_object():
        return response(party.error_message, party.error_code)

    party.edit(name)

    return response(
        '{} updated successfully'.format(party.name), 200, [data])
