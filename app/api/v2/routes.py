from flask_restful import Api, Resource

from . import v2_blueprint, auth_v2_blueprint
from .views import authorization, products

API = Api(v2_blueprint)
API_AUTH = Api(auth_v2_blueprint)

API.add_resource(products.Products, '/products')

API_AUTH.add_resource(authorization.SignUp, '/signup')
API_AUTH.add_resource(authorization.Login, '/login')