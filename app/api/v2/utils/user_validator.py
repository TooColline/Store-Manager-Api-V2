import re

from flask import make_response, jsonify, abort
from validate_email import validate_email

from .. import db


class UserValidator():

    def validate_user_info(self, data):

        self.email = data["email"]
        self.password = data["password"]

        valid_email = validate_email(self.email)

        if self.email == "" or self.password == "":
            Message = "You are missing critical information"
            abort(400, Message)
        if not valid_email:
            Message = "Invalid email"
            abort(400, Message)
        elif len(self.password) < 6 or len(self.password) > 12:
            Message = "Password must range between 6 to 12 characters"
            abort(400, Message)
        elif not any(char.isdigit() for char in self.password):
            Message = "Password must include at least one digit"
            abort(400, Message)
        elif not any(char.isupper() for char in self.password):
            Message = "Password must include at least one upper case character"
            abort(400, Message)
        elif not any(char.islower() for char in self.password):
            Message = "Password must include at least one lower case character"
            abort(400, Message)
        elif not re.search("^.*(?=.*[@#$%^&+=]).*$", self.password):
            Message = "Password must include at least one special charater"
            abort(400, Message)
    
    @staticmethod
    def check_for_duplication(column, table, value):
        """Checks if products already exists"""
        
        query = """
        SELECT {} FROM {} WHERE {}.{} = '{}'
        """.format(column, table, table, column, value)
        
        duplicated = db.select_from_db(query)

        if duplicated:
            abort(make_response(jsonify(
                message="Product already exists"), 400))