import json
from . import base_test
from . import general_helper_functions
from app.api.v2.models import sales
from app.api.v2 import db

class Sales(base_test.BaseTestClass):
    """Tests for sales endpoints"""

    def test_add_sale(self):
        """Test POST /sales""" 

        response = self.app_test_client.post('{}/products'.format(
            self.base_url), json=self.Product, headers=dict(Authorization=self.token),
            content_type='application/json')

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json=self.SaleOrder, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'Sale order made successfully')
    
    def test_add_sale_with_missing_parameters(self):
        """Test if there is a missing parameter when making a sale"""

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={'name': "Carpet"}, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'Bad request. Request missing a required parameter')
    
    def test_add_sale_with_parameters_not_in_list(self):
        """Tests whether the parameters passed when adding a sale is in a list of dictionaries"""

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={
                'items': {
                    'name': 'Carpet',
                    'quantity': 4
                }
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'It should be a list of dictionaries')
    
    def test_add_sale_product_name_not_string(self):
        """Tests if the product name entered is not in string format"""

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={
                'items': [{
                    'name': 1,
                    'quantity': 4
                }]
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], 'The product name should be in a string format')

    def test_add_sale_quantity_not_in_integers(self):
        """Tests for the quantity to be in integer"""

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={
                'items': [{
                    'name': 'Carpet',
                    'quantity': '4'
                }]
            },
            headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
        response)['message'], 'The quantity should be an integer')
    
    def test_add_sale_quantity_not_positive_integers(self):
        """Tests for whether the quantity is an integer above zero"""

        response = self.app_test_client.post('{}/products'.format(
        self.base_url), json=self.Product, headers=dict(Authorization=self.token),
        content_type='application/json')

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={
                'items': [
                    {
                        'name': 'Carpet',
                        'quantity': -1
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "The quantity should be a positive integer")

    def test_add_sale_when_product_not_in_inventory(self):
            """Test POST /sales"""

            response = self.app_test_client.post('{}/products'.format(
            self.base_url), json={
                'name': 'Carpet',
                'price': 55000,
                'min_quantity': 10,
                'inventory': 0,
                'category': 'Home & Furniture'
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

            response = self.app_test_client.post('{}/sales'.format(
                self.base_url), json={
                    'items': [
                        {
                            'name': 'Carpet',
                            'quantity': 1000
                        }
                    ]
                }, headers=dict(Authorization=self.token),
                content_type='application/json')

            self.assertEqual(response.status_code, 400)
            self.assertEqual(general_helper_functions.convert_json(
                response)['message'], "You cannot add Carpet to your order since it is currently out of stock")

        
    def test_get_specific_sale(self):
        """Test GET /sales/<int:sale_id>"""

        self.app_test_client.post('{}/products'.format(
        self.base_url), json=self.Product, headers=dict(Authorization=self.token),
        content_type='application/json')

        self.app_test_client.post(
        '{}/sales'.format(self.base_url), json=self.SaleOrder,
        headers=dict(Authorization=self.token),
        content_type='application/json')

        response = self.app_test_client.get(
            '{}/sales/1'.format(self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(general_helper_functions.convert_json(
        response)['message'], 'Sale record retrieved successfully')
    
    def test_get_specific_sale_not_found(self):

        response = self.app_test_client.get(
            '{}/sales/1000'.format(self.base_url),
            headers=dict(Authorization=self.token),
            content_type='application/json'
            )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
        response)['message'], 'Sale with id 1000 is not found')

    def test_get_sales_not_found(self):
        """Tests when getting sale records yet none has been made yet"""

        response = self.app_test_client.get(
            '{}/sales'.format(self.base_url),

            headers=dict(Authorization=self.token),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Sorry, there are no sales made yet")

    def test_add_sale_order_when_quantity_exceeds_available(self):
        """Test POST /sales"""

        response = self.app_test_client.post('{}/sales'.format(
            self.base_url), json={
                'items': [
                    {
                        'name': 'Carpet',
                        'quantity': 1000
                    }
                ]
            }, headers=dict(Authorization=self.token),
            content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(general_helper_functions.convert_json(
            response)['message'], "Sorry, the product you ordered does not exist in the store.")
