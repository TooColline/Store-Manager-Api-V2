'''This module holds all data and logic of the sales in the application'''

from datetime import datetime
from .. import db

class SalesModel():
    '''Initializes a sale'''

    def __init__(self, sale_id=None, amount=None, sold_by=None):
       self.amount = amount
       self.sold_by = sold_by
       self.sale_id = sale_id

    def save(self):
        query = """
        INSERT INTO sales(amount, sold_by) VALUES(
            {}, '{}'
        )""".format(self.amount, self.sold_by)

        db.insert_to_db(query)

    def put(self):
        query = """
        UPDATE sales SET amount = {} WHERE sale_id = {}
        """.format(self.amount, self.sale_id)

        db.insert_to_db(query)
    def get(self):
        """
            Queries db for user with given username
            Returns user object
        """
        # Query db for user with those params
        query = """
        SELECT * FROM sales"""

        return db.select_from_db(query)

    def revoke_sale(self):
        query = """DELETE FROM sales WHERE sale_id = {}""".format(self.sale_id)
        db.insert_to_db(query)
    
    def fetch_all_the_sales(self):
        """Fetches all the sales from the db"""

        query = """SELECT * FROM sales"""
        return db.select_from_db(query)
    

class SoldItems():
    def __init__(self, sale_id=None, product=None, quantity=None):
        self.product = product
        self.sale_id = sale_id
        self.quantity = quantity

    def save(self):
        query = """
        INSERT INTO solditems(sale_id, product, quantity) VALUES(
            {}, {}, {}
        )""".format(self.sale_id, self.product, self.quantity)

        db.insert_to_db(query)

    def get(self):
        """Queries db for user with those params"""

        query = """
        SELECT * FROM sales"""

        return db.select_from_db(query)