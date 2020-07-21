import json

import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, TEST_USER_EMAIL


class TestValidateEmail:
    """
    Validate Email Tests

    case1: user already exists in system
    case2: user does not exist in system
    """
    faker = Faker()

    def test_case1(self, test_user):
        data = {
            'email': TEST_USER_EMAIL
        }
        url = BASE_URL.format('/v10/validate_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['user_exists']

    def test_case2(self):
        data = {
            'email': self.faker.email()
        }
        url = BASE_URL.format('/v10/validate_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert not response_data['user_exists']