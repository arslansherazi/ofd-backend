import json

import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_USERNAME


class TestChangePassword:
    """
    Change Password Tests

    case1: invalid old password
    case2: password is changed successfully
    case3: login after password change
    case4: password is changed successfully (forgot password) - change new password to old password
    """
    faker = Faker()

    def test_case1(self, test_user):
        data = {
            'email': TEST_USER_EMAIL,
            'old_password': self.faker.password(),
            'new_password': '123123'
        }
        url = BASE_URL.format('/v10/change_password')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Old password is invalid'
        assert not response_data['is_password_updated']

    def test_case2(self):
        data = {
            'email': TEST_USER_EMAIL,
            'old_password': TEST_USER_PASSWORD,
            'new_password': '123123'
        }
        url = BASE_URL.format('/v10/change_password')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Password is updated successfully'
        assert response_data['is_password_updated']

    def test_case3(self):
        data = {
            'username': TEST_USER_USERNAME,
            'password': '123123'
        }
        url = BASE_URL.format('/v10/login')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_logged_in']

    def test_case4(self):
        data = {
            'email': TEST_USER_EMAIL,
            'new_password': TEST_USER_PASSWORD,
            'is_forgot_password': True
        }
        url = BASE_URL.format('/v10/change_password')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Password is updated successfully'
        assert response_data['is_password_updated']