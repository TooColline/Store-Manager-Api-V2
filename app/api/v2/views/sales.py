import os
import jwt
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import general_helper_functions
from ..models import products, users, sales
from ..utils import token_verification, user_validator
from .. import db

class Sales(Resource):
    """Simple class that handles sales endpoints"""

    def post(self):
        """POST /saleorder endpoint"""

        logged_user = token_verification.verify_tokens()

        data = request.get_json()
        general_helper_functions.json_null_request(data)

        try:
            items = data['items']
        except KeyError:
            general_helper_functions.miss_parameter_required()

        if not isinstance(items, (list, )):
            abort(make_response(jsonify(
                message="It should be a list of dictionaries"
                ), 400))

        totalamt = 0
        saleorder = sales.SalesModel(amount=totalamt, sold_by=logged_user)
        saleorder.save()
        query = """SELECT sale_id from sales WHERE amount = 0
        """
        sale_id = db.select_from_db(query)[0]['sale_id']
        for item in items:
            try:
                name = item['name']
                quantity = item['quantity']
            except KeyError:
                general_helper_functions.miss_parameter_required()

            if not isinstance(name, str):
                revoke_sale = sales.SalesModel(sale_id=sale_id)
                revoke_sale.revoke_sale()
                abort(make_response(jsonify(
                    message="The product name should be in a string format"
                ), 400))
            
            if not isinstance(quantity, int):
                revoke_sale = sales.SalesModel(sale_id=sale_id)
                revoke_sale.revoke_sale()
                abort(make_response(jsonify(
                    message="The quantity should be an integer"
                ), 400))

            if quantity < 1:
                revoke_sale = sales.SalesModel(sale_id=sale_id)
                revoke_sale.revoke_sale()
                abort(make_response(jsonify(
                    message="The quantity should be a positive integer"
                ), 400))
            
            query = """SELECT * FROM products WHERE name = '{}'""".format(name)
            product_exists = db.select_from_db(query)
            if product_exists:
                product_id = product_exists[0]['product_id']
                price = product_exists[0]['price']
                inventory = product_exists[0]['inventory']
                if inventory == 0:
                    revoke_sale = sales.SalesModel(sale_id=sale_id)
                    revoke_sale.revoke_sale()
                    return abort(make_response(jsonify(
                    message="You cannot add {} to your order since it is currently out of stock".format(name)
                    ), 400))

                if quantity > inventory:
                     revoke_sale = sales.SalesModel(sale_id=sale_id)
                     revoke_sale.revoke_sale()

                     return abort(make_response(jsonify(
                     message="Sorry, the current stock can only allow an order of {}".format(inventory)
                     ), 400))  
                totalamt += (price * quantity)   
                solditems = sales.SoldItems(sale_id=sale_id, product=product_id, quantity=quantity)
                solditems.save() 
                update_data = sales.SalesModel(amount=totalamt, sold_by=logged_user, sale_id=sale_id)
                update_data.put()

                updated_inventory = (int(inventory) - int(quantity))
                up_query = """UPDATE products SET inventory = {} WHERE product_id = {}""".format(updated_inventory, product_id)
                db.insert_to_db(up_query)
        

            else:
                revoke_sale = sales.SalesModel(sale_id=sale_id)
                revoke_sale.revoke_sale()
                return abort(make_response(jsonify(
                    message = "Sorry, the product you ordered does not exist in the store."
                ), 404))
        return make_response(jsonify({
            "message": "Sale order made successfully",
            "items_sold": items
        }), 201)

    def get(self):
        """GET /sales retrieves all sales"""

        token_verification.verify_tokens()
        
        fetch = sales.SalesModel()
        fetched = fetch.fetch_all_the_sales()

        if not fetched:
            abort(make_response(jsonify({
                "message": "Sorry, there are no sales made yet"
            }), 404))

        response = make_response(jsonify({
            "message": "All the sales have been fetched successfully",
            "sales": fetched
        }), 201)
        
        return response

class FetchSpecificSale(Resource):
    """Simple class to fetch specific sale"""
    def get(self, sale_id):
        """GET /products/<int:sale_id> fetches specific sale"""
        
        token_verification.verify_tokens()
        query = """SELECT * FROM sales WHERE sale_id = '{}'""".format(sale_id)
        fetched_sale = db.select_from_db(query)

        if not fetched_sale:
            return make_response(jsonify({
            "message": "Sale with id {} is not found".format(sale_id),
            }), 404)
        
        return make_response(jsonify({
            "message": "Sale record retrieved successfully",
            "product": fetched_sale
            }), 200)


