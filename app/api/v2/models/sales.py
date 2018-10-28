'''This module holds all data and logic of the sales in the application'''

from datetime import datetime
from .. import db

class SalesModel():
    '''Initializes a sale'''

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.totalamt = (self.quantity * self.price)
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    '''Saves a sale to sale records'''
    def save(self):
        query = """
        INSERT INTO sales(name, price, quantity, totalamt, date_ordered) VALUES(
            '{}', '{}', '{}', '{}', '{}'
        )""".format(self.name, self.price, self.quantity, self.totalamt, self.date)

        db.insert_to_db(query)