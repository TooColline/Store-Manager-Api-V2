import os
import unittest

from app import create_app
from instance.config import config
from . import general_helper_functions
from app.api.v2.db import initialize_db
from app.api.v2.models.users import UserModels
 
class BaseTestClass(unittest.TestCase):
 
    def setUp(self):
        """set up application for testing"""
        
        self.app = create_app(os.getenv('FLASK_ENV'))
        self.base_url = 'api/v2'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test_client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            self.db_url = config['testing'].DB_URL
            initialize_db(self.db_url)

        self.register_admin_test_account()
        self.token = self.login_admin_test()

        self.Product = {
        "name": "Carpet",
        "price": 17000,
        "min_quantity": 7,
        "inventory": 7,
        "category": "Home & Furniture"
        }

        self.SaleOrder = {
        'items': [
            {
                'name': 'Carpet',
                'quantity': 4
            }
        ]
        }
        
    def tearDown(self):
        """tear down dictionaries"""
        with self.app.app_context():
            initialize_db(self.db_url)
        self.app_context.pop()

    def register_admin_test_account(self):
        """Registers an admin user test account"""
        
        
        data = {
        "email": "admin@gmail.com",
        "password": "Password2@"
        }

        return UserModels.create_admin(data)
    
    def register_attendant_test_account(self):
        #Register attendant
        """Registers an attendant test user account"""
            
        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "attendant@gmail.com",
        "role": "attendant",
        "password": "Password2@"
        }, 
        headers={
        "Content-Type": "application/json"
        })

        return res
    
    def login_admin_test(self):
        """Verify's the admin test account"""

        res = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Password2@"
        },
        headers={
        "Content-Type": "application/json"
        })

        auth_token = general_helper_functions.convert_json(
        res)['token']
        
        return auth_token

    def login_attendant_test(self):
        """Validates the test account for the attendant"""

        # Login the test account for the admin
        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "attendant@gmail.com",
            "password": "Password2@"
        },
        headers={
        "Content-Type": "application/json"
        })

        auth_token = general_helper_functions.convert_json(
        resp)['token']

        return auth_token

if __name__ == '__main__':
    unittest.main()