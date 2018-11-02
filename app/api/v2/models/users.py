'''This module holds all data and logic of the users in the application'''

from flask import make_response, jsonify
from .. import db
import psycopg2
from psycopg2 import sql, extras

class UserModels():
    '''Initializes a new user'''
    def __init__(self, email=None, password=None, role=None, token=None):
        self.email = email
        self.password = password
        self.role = role
        self.token = token
        
    def save(self):
        '''Saves a user by appending them to the users table'''
        # db_url = "dbname='store_manager' host='localhost' port='5432' user='postgres' password='Password2#'"
        # conn = psycopg2.connect(db_url)
        # cursor  = conn.cursor()


        query = """
        INSERT INTO users(email, password, role) VALUES(
            '{}', '{}', '{}'
        )""".format(self.email, self.password, self.role)
        db.insert_to_db(query)
        # cursor.execute(query)  
        # conn.commit()
    @staticmethod
    def fetch_user_by_email(email):
        """Queries the db for a user given email"""
        query = """
        SELECT * FROM users
        WHERE email = '{}'""".format(email)

        return db.select_from_db(query)

    @staticmethod
    def checkifuserexists(data):
        if data['email']:
            query="SELECT * FROM users WHERE email = '%s';" % data['email']
            
            return db.select_from_db(query)
        return False

    def logout(self):
        query = """
        INSERT INTO blacklist (token) VALUES ('{}')
        """.format(self.token)

        return db.insert_to_db(query)