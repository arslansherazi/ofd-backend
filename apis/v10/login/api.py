import json

import requests
from django.conf import settings
from django.contrib.auth.hashers import check_password
from requests.auth import HTTPBasicAuth

from apis.v10.login.validator import LoginValidator
from common.base_resource import BasePostResource
from common.constants import BUYER_USER_TYPE
from models.buyer import Buyer
from models.merchant import Merchant
from repositories.v10.user_repo import UserRepository


class Login(BasePostResource):
    version = 10
    end_point = 'login'
    request_validator = LoginValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.username = self.request_args.get('username', '')
        self.password = self.request_args.get('password', '')
        self.user_type = int(self.request_args.get('user_type', ''))

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.is_email_verified = False
        self.is_user_exist = False
        self.is_password_invalid = False
        self.authentication_token = ''

    def check_user_credentials(self):
        """
        Checks user credentials.
        Verifies that username/email exists in system or not and email is verified or not.
        """
        if self.user_type == BUYER_USER_TYPE:
            self.login_info = Buyer.get_buyer_login_info(username=self.username)
        else:
            self.login_info = Merchant.get_merchant_login_info(username=self.username)
        if self.login_info:
            self.is_user_exist = True
            self.process_user_login()
            if self.login_info.get('is_email_verified', False):
                self.is_email_verified = True

    def process_user_login(self):
        """
        Verifies that either user credentials are correct or not
        """
        self.password_hash = self.login_info.get('password')
        if not check_password(self.password, self.password_hash):
            self.is_password_invalid = True

    def generate_authentication_token(self):
        """
        Generates authentication token
        """
        params = {'email': self.login_info.get('email'), 'password': self.password}
        authentication = HTTPBasicAuth('lpHaNdeS', 'KdaAdL$KKJ$Sgf!%ebWp')
        response = requests.post(settings.API_BASE_URL.format('/v10/api_token'), data=params, auth=authentication)
        tokens = json.loads(response.text)
        self.authentication_token = tokens.get('access', '')

    def prepare_response(self):
        """
        Prepares response
        """
        if not self.is_user_exist:
            self.status_code = 422
            self.response = {
                'message': UserRepository.USER_NOT_EXISTS_IN_SYSTEM_MESSAGE,
                'is_logged_in': False
            }
        elif self.is_password_invalid:
            self.status_code = 403
            self.response = {
                'message': UserRepository.USER_LOGGEDIN_ERROR_MESSAGE,
                'is_logged_in': False
            }
        elif not self.is_email_verified:
            self.status_code = 422
            self.response = {
                'message': UserRepository.EMAIL_VERIFICATION_MESSAGE,
                'is_logged_in': False
            }
        else:
            self.generate_authentication_token()
            self.response = {
                'data': {
                    'is_logged_in': True,
                    'auth_token': self.authentication_token,
                    'email': self.login_info.get('email'),
                    'name': self.login_info.get('name'),
                    'username': self.login_info.get('username'),
                    'profile_image_url': self.login_info.get('profile_image_url'),
                    'user_id': self.login_info.get('user_id')
                }
            }
            if self.user_type == BUYER_USER_TYPE:
                self.response['data'].update(
                    first_name=self.login_info.get('first_name'),
                    last_name=self.login_info.get('last_name')
                )

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.check_user_credentials()
        self.prepare_response()
