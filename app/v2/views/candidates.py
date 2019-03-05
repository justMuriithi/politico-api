from flask import request
from app.v2.util.validate import response, response_error, not_admin
from app.v2.models.candidates_model import Candidate
from app.v2.models.offices_model import Office
from app.v2.blueprints import bp
from flask_jwt_extended import (jwt_required)


@bp.route('/offices/register', methods=['POST'])
@jwt_required
def post_candidate():
    message = 'Success'
    status = 200
    response_data = []
    error = True

    restricted = not_admin()
    if restricted:
        return restricted

    """ Create candidate end point """

    data = request.get_json()

    if data:
        try:
            office = data['office']
            party = data['party']
            candidate = data['candidate']

            item = Candidate(party, office, candidate)

            if item.validate_object():
                item.save()

                # return added candidate
                message = "Success"
                response_data = [item.as_json()]
                status = 201
                error = False
            else:
                message = item.error_message
                status = item.error_code

        except KeyError as e:
            message = "{} field is required".format(e.args[0])
            status = 400
    else:
        message = "No data was provided"
        status = 400

    if error:
        return response_error(message, status)
    else:
        return response(message, status, response_data)


@bp.route('/candidates', methods=['GET'])
@jwt_required
def get_candidates():
    """ Get all candidates end point """

    return response('Success', 200, Candidate().load_all())


@bp.route('/candidates/<int:id>', methods=['GET'])
@jwt_required
def get_candidate(id):
    """ Get single candidate end point """

    model = Candidate()
    data = model.find_by('id', id)

    if not data:
        return response_error('Candidate not found', 404)

    return response('Success', 200, [data])


@bp.route('/offices/<int:office_id>/candidates', methods=['GET'])
@jwt_required
def get_office_candidates(office_id):
    """ Get all candidates of a certain office end point """

    if not Office().find_by('id', office_id):
        return response_error('Selected Office does not exist', 404)

    return response(
        'Success', 200, Candidate().find_all_by('office', office_id))
