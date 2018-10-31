'''This module holds all data and logic of the products in the application'''

from datetime import datetime
from .. import db


class ProductsModel():
    '''Initializes a new product'''
    def __init__(self, product_id=None, name=None, price=None, category=None):
        self.product_id = product_id
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
    
    def fetch_all_the_products(self):
        """Fetches all the products from the db"""

        query = """SELECT * FROM products"""
        return db.select_from_db(query)

    def put(self):
        query = """UPDATE products SET name = '{}', price = '{}',
        category = '{}' WHERE product_id = {}""".format(self.name, self.price,
                                                        self.category, self.product_id)

        db.insert_to_db(query)