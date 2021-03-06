"""This module contains tests to user authentication endpoints"""

import json

from . import base_test
from . import general_helper_functions
from app.api.v2.db import initialize_db

class TestUserAuthEndpoints(base_test.BaseTestClass):

    def test_missing_token(self):
        """Test GET /products - when token is missing"""
        token = ""

        response = self.app_test_client.get(
            '{}/products'.format(self.base_url),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(general_helper_functions.convert_json(
            response)["Message"], "You need to login")

    

    def test_add_new_user_with_all_data(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "newuser@gmail.com",
        "role": "Admin",
        "password": "Password1@"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['user']['email'], "newuser@gmail.com")
        self.assertEqual(res.status_code, 200)
    
    def test_add_new_user_already_existing(self):
        """Test POST /auth/signup"""
        
        response = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "admin@gmail.com",
        "role": "Admin",
        "password": "Password2#"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 409)
        self.assertEqual(data['message'], "User with that email already exists")

    def test_add_new_user_with_no_data(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={}, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(res)

        self.assertEqual(data['message'], "Missing critical credentials")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_with_some_missing_parameter(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "",
        "role": "Admin",
        "password": "Password2#"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "You are missing critical information")
        self.assertEqual(res.status_code, 400)
    
    def test_add_new_user_short_password(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "testnewuser@gmail.com",
        "role": "Admin",
        "password": "Less#"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must range between 6 to 12 characters")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_with_invalid_email(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "newuser",
        "role": "Admin",
        "password": "Password12#"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Invalid email")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_with_no_digit_in_password(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "testnewuser@gmail.com",
        "role": "Admin",
        "password": "@Nodigit"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must include at least one digit")
        self.assertEqual(res.status_code, 400)
    
    def test_add_new_user_with_no_upper_case_in_password(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "testingnewuser@gmail.com",
        "role": "Admin",
        "password": "noupper2@"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must include at least one upper case character")
        self.assertEqual(res.status_code, 400)
    
    def test_add_new_user_with_no_lower_case_in_password(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "testingnewuser@gmail.com",
        "role": "Admin",
        "password": "NOLOWER2@"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must include at least one lower case character")
        self.assertEqual(res.status_code, 400)

    def test_add_new_user_with_no_special_char_in_password(self):

        res = self.app_test_client.post("api/v2/auth/signup",
        json={
        "email": "testingnewuser@gmail.com",
        "role": "Admin",
        "password": "Nospecial2"
        }, 
        headers=dict(Authorization=self.token),
            content_type='application/json')

        data = json.loads(res.data.decode())
        print(data)

        self.assertEqual(data['message'], "Password must include at least one special charater")
        self.assertEqual(res.status_code, 400)
    
    def test_login_with_no_credentials(self):

        resp = self.app_test_client.post("api/v2/auth/login",
        json={

        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(general_helper_functions.convert_json(
        resp)['message'], "Kindly provide your credentials")
        self.assertEqual(resp.status_code, 400)
 
    def test_login_already_existing_user(self):

        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "Password2@"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(general_helper_functions.convert_json(
        resp)['token'])
        self.assertTrue(general_helper_functions.convert_json(
        resp)['message'], "You are successfully logged in!")
        self.assertEqual(resp.status_code, 200)
    
    def test_login_user_not_existing_with_email(self):

        resp = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "userwrongcredentials@gmail.com",
            "password": "notevensureofpassword"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertEqual(general_helper_functions.convert_json(
        resp)['message'], "Sorry, cannot find user with that email")
    
    def test_user_login_with_wrong_password(self):

        response = self.app_test_client.post("api/v2/auth/login",
        json={
            "email": "admin@gmail.com",
            "password": "notevensureofpassword"
        },
        headers={
        "Content-Type": "application/json"
        })

        self.assertTrue(general_helper_functions.convert_json(
        response)['message'], "Wrong credentials entered please try again")
        self.assertEqual(response.status_code, 403)

    def test_logout_user(self):

        response = self.app_test_client.post('{}/auth/logout'.format(
            self.base_url), headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Logged out successfully"
        )
    
    # def test_abort_user_if_not_admin(self):
    #     token = self.login_attendant_test()

    #     response = self.app_test_client.post('{}/products'.format(
    #         self.base_url), json={'name': 'Carpet', 'price': 17000, 'min_quantity': 7, 'inventory': 7,
    #         'category': 'Home & Furniture'}, headers=dict(Authorization=token),
    #         content_type='application/json')

    #     self.assertEqual(general_helper_functions.convert_json(
    #     response)['message'], "Unauthorized access, please contact your administrator!")
    #     self.assertEqual(response.status_code, 401)

    def test_invalid_token_provided(self):

        token = "invalid.token.provided"
        response = self.app_test_client.get(
            '{}/products'.format(self.base_url),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(general_helper_functions.convert_json(
            response)["Message"], "This token is invalid")
    