import json
from . import base_test
from . import general_helper_functions
from app.api.v2.models import products
from app.api.v2 import db

class Products(base_test.BaseTestClass):
    """Tests products specific endpoints"""

    def test_add_new_product(self):
        """Test POST /products request"""

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['name'], self.Product['name'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['price'], self.Product['price'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['min_quantity'], self.Product['min_quantity'])
        
        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['inventory'], self.Product['inventory'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['category'], self.Product['category'])

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'Product has been added successfully')

    def test_add_new_product_price_negative(self):
        """Test POST /products with the price of a negative number or zero"""

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': "Hand Bag", 'price': -1, 'min_quantity': 7, 'inventory': 7, 'category':'Clothing'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Price of the product should be a positive integer')

    def test_add_new_product_missing_parameter(self):

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': "Hand Bag", 'price': -1, 'inventory': 7, 'category':'Clothing'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Bad request. Request missing a required parameter')

    def test_add_new_product_name_not_string(self):
        """Test POST /products with a product name different from string"""

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': 5, 'price': 100, 'min_quantity': 7, 'inventory': 7, 'category':'Clothing'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Product name should be in a string format')
    
    def test_add_new_product_category_not_string(self):
        """Test POST /products with the category not in a string format"""

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': "Hand Bag", 'price': 10, 'min_quantity': 7, 'inventory': 7, 'category':20
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Category should be in a string format')

    def test_add_new_product_product_already_existing_in_db(self):
        """Test POST /products with a product name that already exists"""

        self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': "Hand Bag", 'price': 10, 'min_quantity': 7, 'inventory': 7, 'category':'Clothing'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': "Hand Bag", 'price': 10, 'min_quantity': 7, 'inventory': 7, 'category':'Clothing'
                }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Product already exists')
    def test_get_all_products(self):
        """Test GET /products - when products exist"""

        # send a dummy data response for testing
        self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=self.token),
            content_type='application/json')


        response = self.app_test_client.get(
            '{}/products'.format(self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(general_helper_functions.convert_json(
            response)['products'][0]['name'], self.Product['name'])
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'All the products have been fetched successfully')

    def test_get_all_products_not_found(self):

        response = self.app_test_client.get(
            '{}/products'.format(self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Sorry, there are no products in the database yet')
    
    def test_get_specific_product(self):
        """Test GET /products/<int:product_id> if the product is available in store"""

        insert_dummy_product = """INSERT INTO products (name, price, min_quantity, inventory, category)
        VALUES ('Carpet', 17000, 7, 7, 'Home & Furniture')"""
        db.insert_to_db(insert_dummy_product)

        query = """SELECT * FROM products WHERE name = 'Carpet'"""
        product_id = db.select_from_db(query)
        response = self.app_test_client.get(
            '{}/products/{}'.format(self.base_url, product_id[0]['product_id']),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
            response)['product'][0]['name'], 'Carpet')
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Carpet retrieved successfully')
        
    
    def test_get_specific_product_not_existing(self):
        """Test GET /products/<int:product_id> - when product does not exist"""

        response = self.app_test_client.get(
            '{}/products/1000'.format(self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'],
            'Product with id 1000 is not existing')
        
    def test_modify_product(self):
        """PUT /product/"""

        self.app_test_client.post('{}/products'.format(
            self.base_url), json={'name': 'Carpet', 'price': 17000, 'min_quantity': 7, 'inventory': 7,
            'category': 'Home & Furniture'}, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE name = 'Carpet'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.put('{}/products/{}'.format(
            self.base_url, product_id[0]['product_id']),
             json={
                 'name':'Bedcover',
                 'price': 1500,
                 'category':'Beddings',
                 'min_quantity': 7,
                 'inventory': 7
             },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 202)
        self.assertEqual(general_helper_functions.convert_json(
            response)['product']['name'], "Bedcover")

    def test_modify_product_with_missing_parameter(self):
        """PUT /product/"""

        self.app_test_client.post('{}/products'.format(
            self.base_url), json={'name': 'Carpet', 'price': 17000, 'min_quantity': 7, 'inventory': 7,
            'category': 'Home & Furniture'}, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE name = 'Carpet'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.put('{}/product/{}'.format(
            self.base_url, product_id[0]['product_id']),
             json={
                 'name':'Sheet',
                 'category':'Bedding Cover'
             },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
    
    def test_request_not_json_format(self):
        """Test POST /products"""
        
        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=self.token),
            content_type='application/text')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'Bad request. Request must be in json format')


    def test_delete_product(self):
        """DELETE /product/id"""

        self.app_test_client.post('{}/products'.format(
            self.base_url), json={'name': 'Carpet', 'price': 17000, 'min_quantity': 7, 'inventory': 7,
            'category': 'Home & Furniture'}, headers=dict(Authorization=self.token),
            content_type='application/json')

        query = """SELECT product_id FROM products WHERE name = 'Carpet'"""
        product_id = db.select_from_db(query)

        response = self.app_test_client.delete('{}/products/{}'.format(
            self.base_url, product_id[0]['product_id']),
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Product has been deleted successfully")
    
    def test_delete_product_not_existing(self):
        """DELETE /products/<int:product_id>"""

        response = self.app_test_client.delete('{}/products/1000'.format(
            self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Product of id 1000 is not available")