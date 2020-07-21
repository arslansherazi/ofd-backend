import json

import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL


class TestSignup:
    """
    Signup Tests

    case1: successful signup
    case2: username is not available
    case3: email already exist in the system
    """
    faker = Faker()
    username = 'test_{}'.format(faker.user_name())
    email = 'test_{}'.format(faker.email())

    def test_case1(self):
        data = {
            'username': self.username,
            'email': self.email,
            'password': '123456',
            'user_type': 1,
            'address': 'Sialkot'
        }
        url = BASE_URL.format('/v10/signup')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'user is signed up successfully'
        assert response_data['is_signed_up']

    def test_case2(self):
        data = {
            'username': self.username,
            'email': self.email,
            'password': '123456',
            'user_type': 1,
            'address': 'Sialkot'
        }
        url = BASE_URL.format('/v10/signup')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'username already exists'
        assert not response_data['is_signed_up']

    def test_case3(self):
        data = {
            'username': self.faker.user_name(),
            'email': self.email,
            'password': '123456',
            'user_type': 1,
            'address': 'Sialkot'
        }
        url = BASE_URL.format('/v10/signup')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'email already registered with us. Please register with some other email'
        assert not response_data['is_signed_up']
