import os
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask import Flask, jsonify, request, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity
)

from instance import config
from ..utils.user_validator import UserValidator
from ..utils import token_verification
from ..models import users

class SignUp(Resource):
    """Simple class that holds signup methods"""
    def post(self):
        """POST /auth/signup"""
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                                    "message": "Missing critical credentials"
                                    }), 400)
        try:
            request_user_email = data["email"].strip()
            request_user_password = data["password"].strip()
            request_user_role = data["role"].strip()
        except KeyError:
            return make_response(jsonify({
                        "message": "Your credentials are missing either your email, password or role"
                        }), 400)

        UserValidator.validate_user_info(self, data)
        hashed_password = generate_password_hash(request_user_password, method='sha256')
        user = users.UserModels(email=request_user_email, password=hashed_password, role=request_user_role)

        if user.checkifuserexists(data):
            return make_response(jsonify({'message': 'User with that email already exists'}), 409)
        else:
            user.save()
            return make_response(jsonify({
                "message": "User account created successfully",
                "user": {
                    "email": request_user_email,
                    "role": request_user_role
                }
            }), 200)


class Login(Resource):
    def post(self):
        """POST /auth/login"""
        data = request.get_json()
        if not data:
            return make_response(jsonify({
                "message": "Kindly input your login credentials"
            }
            ), 400)

        request_user_email = data["email"].strip()
        request_user_password = data["password"].strip()

        user = users.UserModels.fetch_user_by_email(request_user_email)
        if not user:
            abort(make_response(jsonify({
                "message": "Sorry, cannot find user with that email"}), 404))

        users_email = user[0][1]
        users_password = user[0][2]

        if request_user_email == users_email and check_password_hash(users_password, request_user_password):
            token = jwt.encode({
                "email": request_user_email,
                "exp": datetime.datetime.utcnow() + datetime.timedelta
                                (minutes=30)
            }, os.getenv('JWT_SECRET_KEY', default='thisissecret'))
            return make_response(jsonify({
                            "message": "Successfully logged in",
                            "token": token.decode("UTF-8")}), 200)
        return make_response(jsonify({
            "message": "Wrong credentials entered please try again"
        }
        ), 403)

class Logout(Resource):
    def post(self):
        token = request.headers['Authorization']
        user = users.UserModels(token=token)
        user.logout()

        return make_response(jsonify({
            'message': 'Logged out successfully'
        }), 200)