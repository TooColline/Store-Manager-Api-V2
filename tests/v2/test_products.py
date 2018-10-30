import json
from . import base_test
from . import general_helper_functions

class Products(base_test.BaseTestClass):
    """Tests products specific endpoints"""

    def test_add_new_product(self):
        """Test POST /products request"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['name'], self.Product['name'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['price'], 17000)

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['category'], self.Product['category'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'Product has been added successfully')

    def test_add_new_product_price_negative(self):
        """Test POST /products with the price of a negative number or zero"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'product_id': 1, 'name': "Hand Bag", 'price': 0, 'category':'Clothing'
                }, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Price of the product should be a positive integer')

    def test_add_new_product_name_not_string(self):
        """Test POST /products with a product name different from string"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'product_id': 1, 'name': 2, 'price': 200, 'category':'Accessories'
                }, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Product name should be in a string format')
    
    def test_add_new_product_category_not_string(self):
        """Test POST /products with the category not in a string format"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'product_id': 1, 'name': "Shoes", 'price': 1000, 'category': 15
                }, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Category should be in a string format')

    def test_add_new_product_product_already_existing_in_db(self):
        """Test POST /products with a product name that already exists"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'product_id': 1, 'name': 'Hand Bag', 'price': 1500, 'category': 'Clothing'
                }, headers=dict(Authorization=token),
            content_type='application/json')

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'product_id': 1, 'name': "Hand Bag", 'price': 1500, 'category': "Clothing"
                }, headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Sorry. A product with a similar name already exists in the database.')
