from flask import request
from app.v2.models.offices_model import Office
from app.v2.models.user_model import User
from app.v2.models.vote_model import Vote
from app.v2.util.validate import response, response_error
from app.v2.blueprints import bp
from flask_jwt_extended import (jwt_required, get_jwt_identity)


@bp.route('/votes', methods=['POST', 'GET'])
@jwt_required
def vote():
    if request.method == 'POST':
        """ Create vote end point """

        data = request.get_json()

        if not data:
            return response_error("No data was provided", 400)

        try:
            created_by = get_jwt_identity()
            office = data['office']
            candidate = data['candidate']
        except KeyError as e:
            return response_error("{} field is \
            required".format(e.args[0]), 400)

        vote = Vote(created_by, office, candidate)

        if not vote.validate_object():
            return response_error(vote.error_message, vote.error_code)

        if not Office().find_by('id', office):
            return response_error('Selected Office does not exist', 404)
        if not User().find_by('id', candidate):
            return response_error('Selected User does not exist', 404)

        vote.save()

        # return added vote
        return response("Success", 201, [vote.as_json()])

    elif request.method == 'GET':
        """ Get all votes end point """

        return response('Success', 200, Vote().load_all())


@bp.route('/votes/candidate/<int:id>', methods=['GET'])
@jwt_required
def get_candidate_votes(id):
    """ Gets all votes for a specific candidate """

    obtained = [Vote().find_all_by('candidate', id)]

    return response(
        'Success', 200, obtained)


@bp.route('/offices/<int:id>/result', methods=['GET'])
@jwt_required
def get_office_votes(id):
    """ Gets all votes for a specific office """

    obtained = Vote().get_all(
        """
        SELECT concat_ws(' ', users.firstname, users.lastname) AS candidate,
        offices.name as office,
         (SELECT COUNT(*)
            FROM votes AS p
            WHERE p.candidate = e.candidate
            GROUP BY p.candidate
         ) AS results,
         (
             SELECT parties.name FROM candidates as h
             INNER JOIN parties ON parties.id = h.party
             WHERE h.id = e.candidate
         ) as party
         FROM votes AS e
         INNER JOIN users ON users.id = e.candidate
         INNER JOIN offices ON offices.id = e.office
         WHERE office = '{}'
         GROUP BY e.candidate, users.firstname, users.lastname, offices.name
         ORDER BY results DESC
        """.format(id)
    )

    return response('Success', 200, obtained)


@bp.route('/voting-history', methods=['GET'])
@jwt_required
def voting_history():
    """ Gets voting history for current user """

    current_user = get_jwt_identity()

    obtained = Vote().get_all(
        """
        SELECT concat_ws(' ', users.firstname, users.lastname) AS candidate,
        offices.name as office,
         (SELECT COUNT(*)
            FROM votes AS p
            WHERE p.candidate = e.candidate
            GROUP BY p.candidate
         ) AS results,
         (
             SELECT parties.name FROM candidates as h
             INNER JOIN parties ON parties.id = h.party
             WHERE h.id = e.candidate
         ) as party,
         (SELECT COUNT(*)
            FROM votes AS p
            WHERE p.office = e.office
            GROUP BY p.office
         ) AS total_votes
         FROM votes AS e
         INNER JOIN users ON users.id = e.candidate
         INNER JOIN offices ON offices.id = e.office
         WHERE createdBy = '{}'
         GROUP BY e.candidate, users.firstname, users.lastname, offices.name,
         e.office
        """.format(current_user)
    )

    return response('Success', 200, obtained)
