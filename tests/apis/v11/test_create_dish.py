import json

import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, TEST_USER_USERNAME


class TestCreateDish:
    """
    Create Dish Tests

    case1: create dish successfully
    case2: dish already exists
    case2: limit of dishes exceeded
    """
    faker = Faker()

    def test_case1(self, test_user, remove_dishes):
        data = {
            'username': TEST_USER_USERNAME,
            'name': 'test_dish',
            'price': 200,
            'unit': 'grams',
            'quantity': 250,
            'ingredients': [
                {
                    'name': 'alo',
                    'quantity': 250,
                    'unit': 'grams'
                },
                {
                    'name': 'onion',
                    'quantity': 150,
                    'unit': 'grams'
                }
            ],
            'photo': 'menu_item.jpeg'
        }
        url = BASE_URL.format('/v10/create_menu_item')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Your dish is offered successfully'

    def test_case2(self):
        data = {
            'username': TEST_USER_USERNAME,
            'name': 'test_dish',
            'price': 200,
            'unit': 'grams',
            'quantity': 250,
            'ingredients': [
                {
                    'name': 'alo',
                    'quantity': 250,
                    'unit': 'grams'
                },
                {
                    'name': 'onion',
                    'quantity': 150,
                    'unit': 'grams'
                }
            ],
            'photo': 'menu_item.jpeg'
        }
        url = BASE_URL.format('/v10/create_menu_item')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'test dish is already offered'

    def test_case3(self, add_dishes):
        data = {
            'username': 'test_user',
            'name': self.faker.name(),
            'price': 200,
            'unit': 'grams',
            'quantity': 250,
            'ingredients': [
                {
                    'name': 'alo',
                    'quantity': 250,
                    'unit': 'grams'
                },
                {
                    'name': 'onion',
                    'quantity': 150,
                    'unit': 'grams'
                }
            ],
            'photo': 'menu_item.jpeg'
        }
        url = BASE_URL.format('/v10/create_menu_item')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Sorry, You cannot offer more than 6 dishes'
