from flask import Blueprint, request, jsonify, make_response

bp = Blueprint('api', __name__, url_prefix='/api/version1')

parties = []
offices = []

@bp.route('/parties', methods=['POST', 'GET'])
def create_party():
    if request.method == 'POST':
        """ end point for create_party """

        data = request.get_json()

        try:
            name = data['name']
            hqAddress = data['hqAddress']
            logo_url = data['logo_url']
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        party = {
            "id": generate_unique_id(parties),
            "name": name,
            "hqAddress": hqAddress,
            "logo_url": logo_url
        }

        parties.append(party)
        # return new list of parties
        return response('Your political party was created successfully', 201, party)

    elif request.method == 'GET':
        """ end point for get parties """

        return response('Request was successful', 200, parties)


@bp.route('/offices', methods=['POST', 'GET'])
def create_office():
    if request.method == 'POST':
        """ end point for create_office """

        data = request.get_json()

        try:
            category = data['category']
            name = data['name']
    
        except KeyError as e:
            return response("{} field is required".format(e.args[0]), 400)

        office = {
            "id": generate_unique_id(offices),
            "category": category,
            "name": name
        }

        offices.append(office)
        # return new list of offices
        return response('Your political office was created successfully', 201, office)

    elif request.method == 'GET':
        """ end point for get offices """

        return response('Request was successful', 200, offices)

@bp.route('/parties/<int:id>', methods=['GET', 'DELETE'])
def get_party(id):

    obtained = filter (lambda party: party['id'] == id, parties)
    obtained = list(obtained)

    if len(obtained) == 0:
        return response('Party not found', 404, [])

    if request.method == 'GET':
        return response('Request was successful', 200, obtained)

    else:
        for p in range(len(parties)):
            if parties[p]['id'] == id:
                party = parties.pop(p)
                break
        return response(
            '{} deleted successfully'.format(party['name']), 200, [party])

@bp.route('/parties/<int:id>/<string:name>', methods=['PATCH'])
def edit_party(id, name):

    obtained = filter (lambda party: party['id'] == id, parties)
    obtained = list(obtained)

    if len(obtained) == 0:
        return response('Party not found', 404, [])

    
    for p in range(len(parties)):
        if parties[p]['id'] == id:
            party = parties[p]
            party['name'] = name
            parties[p] = party
            break
    return response(
        '{} updated successfully'.format(party['name']), 200, [party])

def generate_unique_id(list):
    """ unique ID creation for a new item to be added to the list"""

    return len(list) + 1


def response(message, code, data=None):
    """ Creates a basic reposnse """
    response = {
        "status": code,
        "message": message,
        "data": data
    }
    return make_response(jsonify(response), code)