from flask import Blueprint

v2_blueprint = Blueprint('v2_blueprint', __name__)
auth_v2_blueprint = Blueprint('auth_v2_blueprint', __name__)

from . import routes