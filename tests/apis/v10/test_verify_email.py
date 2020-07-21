import json
import random
from datetime import timedelta, datetime

import pytest
import requests
from faker import Faker
from requests.auth import HTTPBasicAuth

from tests.apis.constants import BASE_URL, TEST_USER_EMAIL, TEST_USER_USERNAME, DB_CONFIGS
from wrappers.py_sql import PySQL


class TestVerifyEmail:
    """
    Verify Email Tests

    (Email Verification)
    case1: invalid verification code
    case2: verification code is expired
    case3: email is verified successfully

    (Email Verification in case of Forgot Password)
    case4: invalid verification code
    case5: verification code is expired
    case6: email is verified successfully
    """
    faker = Faker()

    @pytest.fixture
    def expire_email_verification_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET email_verification_code_expiration = %s
        WHERE username = %s
        """
        expired_time = datetime.utcnow() - timedelta(minutes=10)
        py_sql.params = [expired_time, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def add_email_verification_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET email_verification_code = %s
        WHERE username = %s
        """
        email_verification_code = random.randrange(100000, 999999, 1)
        py_sql.params = [email_verification_code, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def add_forgot_password_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET forgot_password_code = %s
        WHERE username = %s
        """
        forgot_password_code = random.randrange(100000, 999999, 1)
        py_sql.params = [forgot_password_code, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def remove_email_verification_code_expiration(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET email_verification_code_expiration = %s
        WHERE username = %s
        """
        expired_time = datetime.utcnow() + timedelta(minutes=10)
        py_sql.params = [expired_time, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def email_verification_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        SELECT email_verification_code
        FROM user
        WHERE username = %s
        """
        py_sql.params = [TEST_USER_USERNAME]
        user_data = py_sql.fetch_one()
        return user_data.get('email_verification_code')

    @pytest.fixture
    def expire_forgot_password_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        UPDATE user 
        SET forgot_password_code_expiration = %s
        WHERE username = %s
        """
        expired_time = datetime.utcnow() - timedelta(minutes=10)
        py_sql.params = [expired_time, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def remove_forgot_password_code_expiration(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
            UPDATE user 
            SET forgot_password_code_expiration = %s
            WHERE username = %s
            """
        expired_time = datetime.utcnow() + timedelta(minutes=10)
        py_sql.params = [expired_time, TEST_USER_USERNAME]
        py_sql.save_changes()

    @pytest.fixture
    def forgot_password_code(self):
        py_sql = PySQL(**DB_CONFIGS)
        py_sql.query = """
        SELECT forgot_password_code
        FROM user
        WHERE username = %s
        """
        py_sql.params = [TEST_USER_USERNAME]
        user_data = py_sql.fetch_one()
        return user_data.get('forgot_password_code')

    def test_case1(self, test_user, add_email_verification_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': random.randrange(100000, 999999, 1),
            'is_email_verification_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        print(response_data)
        assert response_data['message'] == 'Verification code is invalid'
        assert not response_data['is_email_verified']

    def test_case2(self, expire_email_verification_code, email_verification_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': email_verification_code,
            'is_email_verification_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        print(response_data)
        assert response_data['message'] == 'Verification code is expired'
        assert not response_data['is_email_verified']

    def test_case3(self, remove_email_verification_code_expiration, email_verification_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': email_verification_code,
            'is_email_verification_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_email_verified']

    def test_case4(self, add_forgot_password_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': random.randrange(100000, 999999, 1),
            'is_forgot_password_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        print(response_data)
        assert response_data['message'] == 'Verification code is invalid'
        assert not response_data['is_email_verified']

    def test_case5(self, expire_forgot_password_code, forgot_password_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': forgot_password_code,
            'is_forgot_password_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['message'] == 'Verification code is expired'
        assert not response_data['is_email_verified']

    def test_case6(self, remove_forgot_password_code_expiration, forgot_password_code):
        data = {
            'email': TEST_USER_EMAIL,
            'code': forgot_password_code,
            'is_forgot_password_code': True
        }
        url = BASE_URL.format('/v10/verify_email')
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(url, data=data, auth=authentication)
        response_data = json.loads(response.text)
        assert response_data['is_email_verified']
