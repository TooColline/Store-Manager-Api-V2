from flask import jsonify, abort, make_response
from flask_restful import Resource

from datetime import datetime
from .. import db

def json_null_request(data):
    """Abort, if data has no json object."""
        
    if data is None:
        abort(make_response(jsonify(
            message="Bad request. Request must be in json format"), 400))

def miss_parameter_required():
    """Abort, if data is missing a required parameter."""

    abort(make_response(jsonify(
        message="Bad request. Request missing a required parameter"), 400))

def abort_user_if_not_admin(user):
    try:
        query = """SELECT role FROM users WHERE email = '{}'""".format(user)
        user_role = db.select_from_db(query)
        if user_role[0][0] != "Admin":
            abort(make_response(jsonify(
                message="Unauthorized access, please contact your administrator!"
            ), 401))
    except:
        abort(make_response(jsonify(
            message="Invalid token"
        ), 401))