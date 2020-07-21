import json

import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import (BASE_URL, TEST_USER_PASSWORD,
                                  TEST_USER_USERNAME)


class TestDishesListing:
    """
    Dishes Listing Tests

    case1: user does not offer any dish yet
    case2: user dishes listing
    """
    faker = Faker()

    def test_case1(self, test_user, remove_dishes):
        data = {
            'username': TEST_USER_USERNAME,
            'password': TEST_USER_PASSWORD,
        }
        url = BASE_URL.format('/v10/menus_listing')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'You did not offer any dish yet'

    def test_case2(self, user_id, add_dishes):
        data = {
            'user_id': user_id
        }
        url = BASE_URL.format('/v10/menus_listing')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['data']['dishes']
