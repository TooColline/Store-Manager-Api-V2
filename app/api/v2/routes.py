from flask_restful import Api, Resource

from . import v2_blueprint, auth_v2_blueprint

API = Api(v2_blueprint)
API_AUTH = Api(auth_v2_blueprint)