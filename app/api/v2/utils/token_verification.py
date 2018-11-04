import os
import jwt
from functools import wraps

from flask import request, make_response, jsonify, abort
from .. import db


def verify_tokens():
        token = None
        token = """SELECT"""
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            abort(make_response(jsonify({
                                 "Message": "You need to login"}), 401))
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY', default='thisissecret'), algorithms=['HS256'])
            return data['email']

        except:
            print(os.getenv('JWT_SECRET_KEY', default='thisissecret'))
            abort(make_response(jsonify({
                "Message": "This token is invalid"
            }), 403))

def verify_post_product_fields(price, name, category, min_quantity, inventory):
    if not isinstance(price, int):
        abort(make_response(jsonify(
            message="Product price should be an integer"
        ), 400))

    if price < 1:
        abort(make_response(jsonify(
            message="Price of the product should be a positive integer"
        ), 400))

    if not isinstance(name, str):
        abort(make_response(jsonify(
            message="Product name should be in a string format"
        ), 400))

    if not isinstance(category, str):
        abort(make_response(jsonify(
            message="Category should be in a string format"
        ), 400))
    
    if not isinstance(min_quantity, int):
        abort(make_response(jsonify(
            message="The minimun quantity should be an integer"
        ), 400))
    
    if not isinstance(inventory, int):
        abort(make_response(jsonify(
            message="The inventory should be an integer"
        ), 400))