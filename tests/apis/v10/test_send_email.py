import json

import requests
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, TEST_USER_EMAIL


class TestSendEmail:
    """
    Send Email Tests

    case1: send email of forgot password code
    case2: send email of email verification code
    """
    def test_case1(self, test_user):
        data = {
            'email': TEST_USER_EMAIL,
            'is_forgot_password_code': True
        }
        url = BASE_URL.format('/v10/send_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_email_sent']

    def test_case2(self):
        data = {
            'email': TEST_USER_EMAIL,
            'is_email_verification_code': True
        }
        url = BASE_URL.format('/v10/send_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_email_sent']