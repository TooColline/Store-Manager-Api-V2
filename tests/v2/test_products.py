import json
from . import base_test
from . import general_helper_functions
from app.api.v2.models import products
from app.api.v2 import db

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
    def test_get_all_products(self):
        """Test GET /products - when products exist"""
        self.register_admin_test_account()
        token = self.login_admin_test()

        # send a dummy data response for testing
        self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=token),
            content_type='application/json')


        response = self.app_test_client.get(
            '{}/products'.format(self.base_url),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(general_helper_functions.convert_json(
            response)['products'][0][1], self.Product['name'])
    
    def test_get_specific_product(self):
        """Test GET /products/id - when product exist"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        query = """INSERT INTO products (name, price, category)
        VALUES ('Carpet', 17000, 'Home & Furniture')
        """
        db.insert_to_db(query)
    

        query = """SELECT * FROM products WHERE name = 'Carpet'"""
        product_id = db.select_from_db(query)
        print(product_id[0][0])
        response = self.app_test_client.get(
            '{}/products/{}'.format(self.base_url, product_id[0][0]),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
            response)['product'][0][1], self.Product['name'])
        
    
    def test_get_specific_product_not_existing(self):
        """Test GET /products/<int:product_id> - when product does not exist"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        response = self.app_test_client.get(
            '{}/product/1000'.format(self.base_url),
            headers=dict(Authorization=token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        
    def test_modify_product(self):
        """PUT /product/"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        query = """INSERT INTO products(name, price, category) 
        VALUES('Sheet', 1500, 'Beddings')"""
        
        db.insert_to_db(query)

        query = """SELECT product_id FROM products WHERE name = 'Sheet'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.put('{}/products/{}'.format(
            self.base_url, product_id[0][0]),
             json={
                 'name':'Bedcover',
                 'price': 1500,
                 'category':'Beddings'
             },
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['name'], "Bedcover")

    def test_modify_product_with_missing_parameter(self):
        """PUT /product/"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        query = """INSERT INTO products(name, price, category) 
        VALUES('Sheet', 1500, 'Beddings')"""
        
        db.insert_to_db(query)

        query = """SELECT product_id FROM products WHERE name = 'Sheet'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.put('{}/product/{}'.format(
            self.base_url, product_id[0][0]),
             json={
                 'name':'Sheet',
                 'category':'Bedding Cover'
             },
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_delete_product(self):
        """DELETE /product/id"""

        self.register_admin_test_account()
        token = self.login_admin_test()

        query = """INSERT INTO products(name, price, category) 
        VALUES('Watch', 250, 'Clothing')"""  
        db.insert_to_db(query)

        query = """SELECT product_id FROM products WHERE name = 'Watch'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.delete('{}/products/{}'.format(
            self.base_url, product_id[0][0]),
            headers=dict(Authorization=token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Product has been deleted successfully")