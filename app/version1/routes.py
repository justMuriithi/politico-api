from flask import Blueprint, request, jsonify, make_response

bp = Blueprint('api', __name__, url_prefix='/api/version1')

parties = []


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