'''This module holds all data and logic of the products in the application'''

from datetime import datetime
from .. import db


class ProductsModel():
    '''Initializes a new product'''
    def __init__(self, name, price, category):
        self.name = name
        self.price = price
        self.category = category

    def save(self):
        '''Saves a product by appending it to the products table'''
        query = """
        INSERT INTO products(name, price, category) VALUES(
            '{}', '{}', '{}'
        )""".format(self.name, self.price, self.category)

        db.insert_to_db(query)