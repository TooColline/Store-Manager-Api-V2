import unittest

from app import create_app
from instance.config import config
from . import general_helper_functions
from app.api.v2.db import initialize_db
 
class BaseTestClass(unittest.TestCase):
 
    def setUp(self):
        """set up application for testing"""
        
        self.app = create_app('testing')
        self.base_url = 'api/v2'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app_test_client = self.app.test_client()
        self.app.testing = True

        with self.app.app_context():
            self.db_url = config['test_db_url']
            initialize_db(self.db_url)

        self.Product = {
        'name': 'Carpet',
        'price': 17000,
        'category': 'Home & Furniture'
        }

        self.SaleOrder = {
            'name': 'Carpet',
            'price': 17000,
            'quantity': 2,
            'totalamt': (17000 * 2)
        }
        
    def tearDown(self):
        """tear down dictionaries"""
        with self.app.app_context():
            initialize_db(self.db_url)
        self.app_context.pop()

    def register_admin_test_account(self):
        """Registers an admin user test account"""
            
        resp = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "admin@gmail.com",
        "role": "Admin",
        "password": "Password2@"
        }, 
        headers={
        "Content-Type": "application/json"
        })

        return resp
    
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