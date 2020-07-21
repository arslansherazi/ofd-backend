import json

import pytest
import requests
from faker import Faker
from wrappers.py_sql import PySQL
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, DB_CONFIGS, TEST_USER_USERNAME, TEST_USER_PASSWORD


class TestLogin:
    """
    Login Tests

    case1: email is not verified
    case2: username does not exist in the system
    case3: successful login
    case4: invalid password
    """
    faker = Faker()

    @pytest.fixture
    def verify_email(username):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET is_email_verified = 1
        WHERE username = %s
        """
        py_sql.params = [TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def unverify_email(username):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET is_email_verified = 0
        WHERE username = %s
        """
        py_sql.params = [TEST_USER_USERNAME]
        py_sql.save_changes()

    def test_case1(self, test_user, unverify_email):
        data = {
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD,
        }
        url = BASE_URL.format('/v10/login')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Email is not verified yet'
        assert not response_data['is_logged_in']

    def test_case2(self):
        data = {
            'username': self.faker.user_name(),
            'password': TEST_USER_PASSWORD
        }
        url = BASE_URL.format('/v10/login')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'username does not exist in system'
        assert not response_data['is_logged_in']

    def test_case3(self, verify_email):
        data = {
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD
        }
        url = BASE_URL.format('/v10/login')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_logged_in']

    def test_case4(self):
        data = {
            'username': TEST_USER_USERNAME,
            'password': self.faker.password()
        }
        url = BASE_URL.format('/v10/login')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Password is incorrect'
        assert not response_data['is_logged_in']
