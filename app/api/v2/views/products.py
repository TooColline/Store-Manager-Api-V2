"""This module contains objects for products endpoints"""

import os
import jwt
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required

from . import general_helper_functions
from ..models import products, users
from ..utils import token_verification, user_validator
from .. import db


class Products(Resource):
    """Simple class that holds the products endpoints"""
    
    def post(self):
        """POST /products endpoint"""

        # Token and admin verification
        logged_in_user = token_verification.verify_tokens()
        general_helper_functions.abort_user_if_not_admin(logged_in_user)
        
        data = request.get_json()
        general_helper_functions.json_null_request(data)

        try:
            name = data['name']
            price = data['price']
            category = data['category']
        except KeyError:
            # If the product added is missing a required parameter
            general_helper_functions.miss_parameter_required()

        token_verification.verify_post_product_fields(price, name, category)
        user_validator.UserValidator.check_for_duplication("name", "products", name)

        product_added = products.ProductsModel(name=name, price=price,category=category)
                                          
        product_added.save()

        return make_response(jsonify({
            "message": "Product has been added successfully",
            "product": {
                "name": name,
                "price": price,
                "category": category
            }
        }), 201)
    
    def get(self):
        """GET /products retrieves all products"""

        # token_verification.verify_tokens()
        
        fetch = products.ProductsModel()
        fetched = fetch.fetch_all_the_products()

        if not fetched:
            abort(make_response(jsonify({
                "message": "Sorry, there are no products in the database yet"
            })), 404)

        response = make_response(jsonify({
            "message": "All the products have been fetched successfully",
            "products": fetched
        }), 201)
        
        return response

class FetchSpecificProduct(Resource):
    """Simple class to fetch specific product"""
    def get(self, product_id):
        """GET /products/<int:product_id> fetches specific product"""
        
        token_verification.verify_tokens()
        query = """SELECT * FROM products WHERE product_id = '{}'""".format(product_id)

        fetched_product = db.select_from_db(query)

        if not fetched_product:
            return make_response(jsonify({
            "message": "Product with id {} is not existing".format(product_id),
            }), 404)
        
        return make_response(jsonify({
            "message": "{} retrieved successfully".format(fetched_product[0][1]),
            "product": fetched_product
            }), 200)