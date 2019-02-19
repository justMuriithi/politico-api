from flask import request
from app.version1.models.parties_model import Party
from app.version1.util.validate import response
from app.version1.blueprints import o_bp


parties = Party.parties


@o_bp.route('/parties', methods=['POST', 'GET'])
def create_party():
    if request.method == 'POST':
        """ Create party end point """

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

        # append new party to list
        party.save()

        # return added party
        return response("Your political party was created \
            successfully", 201, [party.as_json()])

    elif request.method == 'GET':
        """ Get all parties end point """

        return response('Request was successful', 200, parties)


@o_bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
def get_party(id):

    model = Party()
    data = model.find_by_id(id)

    if not data:
        return response('Party not found', 404)

    if request.method == 'GET':
        return response('Request was successful', 200, [data])
    else:
        party = model.from_json(data)
        party.delete()
        return response(
            '{} deleted successfully'.format(party.name), 200, [data])


@o_bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
def edit_party(id, name):

    model = Party()
    data = model.find_by_id(id)

    if not data:
        return response('Party not found', 404)

    party = model.from_json(data)
    party.name = name

    if not party.validate_object():
        return response(party.error_message, party.error_code)

    party.edit(name)

    return response(
        '{} updated successfully'.format(party.name), 200, [data])
