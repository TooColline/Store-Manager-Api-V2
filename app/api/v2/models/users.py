'''This module holds all data and logic of the users in the application'''

from datetime import datetime
from .. import db

class UserModels():
    '''Initializes a new user'''
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
        
    def save(self):
        '''Saves a user by appending them to the users table'''
        query = """
        INSERT INTO users(email, role, password) VALUES(
            '{}', '{}', '{}'
        )""".format(self.email, self.role, self.password)

        db.insert_to_db(query)