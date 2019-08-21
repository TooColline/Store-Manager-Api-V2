from flask_restful import Api, Resource

from . import v2_blueprint, auth_v2_blueprint
from .views import authorization, products, sales

API = Api(v2_blueprint)
API_AUTH = Api(auth_v2_blueprint)

API.add_resource(products.Products, '/products')
API.add_resource(products.FetchSpecificProduct, '/products/<int:product_id>')
API.add_resource(sales.Sales, '/sales')
API.add_resource(sales.FetchSpecificSale, '/sales/<int:sale_id>')

API_AUTH.add_resource(authorization.SignUp, '/signup')
API_AUTH.add_resource(authorization.Login, '/login')
API_AUTH.add_resource(authorization.Logout, '/logout')