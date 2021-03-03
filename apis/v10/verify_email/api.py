from django.conf import settings
from django.utils import timezone

from apis.models import User
from apis.v10.verify_email.validator import VerifyEmailValidator
from common.base_resource import BaseGetResource
from common.constants import (CHANGE_PASSWORD_API_ENDPOINT,
                              EMAIL_ALREADY_VERIFIED_MESSAGE,
                              EMAIL_VERIFICATION_LINK_ERROR_MESSAGE,
                              EMAIL_VERIFICATION_MESSAGE, LINK_EXPIRED_MESSAGE,
                              ROUTING_PREFIX, WEB_ROUTING_PREFIX)
from common.security import AESCipher


class VerifyEmail(BaseGetResource):
    version = 10
    end_point = 'verify_email'
    request_validator = VerifyEmailValidator()

    def populate_request_args(self):
        """
        Populates request arguments
        """
        self.user_id = self.request_args.get('user_id')
        self.code = self.request_args.get('code')
        self.is_forgot_password_code = self.request_args.get('is_forgot_password_code')
        self.is_email_verification_code = self.request_args.get('is_email_verification_code')
        self.is_change_email_code = self.request_args.get('is_change_email_code')
        if self.is_change_email_code:
            self.new_email = self.request_args.get('new_email')
            self.old_email = self.request_args.get('old_email')
        if self.is_forgot_password_code:
            self.change_password_token = self.request_args.get('change_password_token')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.is_email_verified = False
        self.is_code_expired = False
        self.is_code_invalid = False
        self.email_already_verified = False
        self.forgot_password_email_verified = False

    def check_verification_code_and_expiration(self, user_code, original_code, code_expiration):
        """
        Verifies email verification code

        :param int user_code: code provided by user
        :param int original_code: code saved in db
        :param datetime code_expiration: code expiration date and time

        :return: code verification
        :rtype: bool
        """
        if not original_code == int(user_code):
            self.is_code_invalid = True
        elif not code_expiration > timezone.now():
            self.is_code_expired = True
        else:
            self.is_email_verified = True

    def verify_email_verification_code_and_expiration(self):
        """
        Verifies email verification code
        """
        if self.is_forgot_password_code:
            forgot_password_data = User.get_forgot_password_email_code_and_expiration(
                self.user_id, self.change_password_token
            )
            if forgot_password_data:
                forgot_password_code = forgot_password_data.get('forgot_password_code')
                forgot_password_code_expiration = forgot_password_data.get('forgot_password_code_expiration')
                self.check_verification_code_and_expiration(
                    self.code, forgot_password_code, forgot_password_code_expiration
                )
                if self.is_email_verified:
                    self.http_response = True
                    api_path = '{routing_prefix}v{version}/{end_point}'.format(
                        routing_prefix=ROUTING_PREFIX, version=self.version,
                        end_point=CHANGE_PASSWORD_API_ENDPOINT
                    )
                    encrypted_api_path = AESCipher.encrypt(api_path)
                    api_url = '{base_url}/{prefix}/{encrypted_api_path}'.format(
                        base_url=settings.BASE_URL, prefix=WEB_ROUTING_PREFIX, encrypted_api_path=encrypted_api_path
                    )
                    encrypted_user_id = AESCipher.encrypt(str(self.user_id))
                    encrypted_change_password_token = AESCipher.encrypt(self.change_password_token)
                    self.response = {
                        'template_name': 'forgot_password_change_template.html',
                        'template_data': {
                            'api_url': api_url,
                            'change_password_token': encrypted_change_password_token,
                            'user_id': encrypted_user_id
                        }
                    }
            else:
                self.http_response = True
                self.response = {
                    'template_name': 'email_verification_message.html',
                    'template_data': {'email_verification_message': LINK_EXPIRED_MESSAGE}
                }
        elif self.is_email_verification_code:
            email_verification_data = User.get_email_verification_code_and_expiration(self.user_id)
            if not email_verification_data.get('is_email_verified'):
                email_verification_code = email_verification_data.get('email_verification_code')
                email_verification_code_expiration = email_verification_data.get('email_verification_code_expiration')
                self. check_verification_code_and_expiration(
                    self.code, email_verification_code, email_verification_code_expiration
                )
                if self.is_email_verified:
                    User.update_email_verification_status(self.user_id)
            else:
                self.email_already_verified = True
        else:
            email_change_data = User.get_change_email_code_and_expiration(self.user_id, self.old_email)
            if email_change_data:
                change_email_code = email_change_data.get('change_email_code')
                change_email_code_expiration = email_change_data.get('change_email_code_expiration')
                self.check_verification_code_and_expiration(
                    self.code, change_email_code, change_email_code_expiration
                )
                if self.is_email_verified:
                    User.change_user_email(self.user_id, self.new_email)
            else:
                self.email_already_verified = True

    def generate_response(self):
        """
        Prepares response
        """
        self.http_response = True
        self.response = {
            'template_name': 'email_verification_message.html',
            'template_data': {}
        }
        if self.email_already_verified:
            self.response.get('template_data')['email_verification_message'] = EMAIL_ALREADY_VERIFIED_MESSAGE
        elif self.is_code_expired:
            self.response.get('template_data')['email_verification_message'] = LINK_EXPIRED_MESSAGE
        elif self.is_code_invalid:
            self.response.get('template_data')['email_verification_message'] = EMAIL_VERIFICATION_LINK_ERROR_MESSAGE
        else:
            self.response.get('template_data')['email_verification_message'] = EMAIL_VERIFICATION_MESSAGE

    def process_request(self):
        """
        Process request
        """
        self.populate_request_args()
        self.initialize_class_attributes()
        self.verify_email_verification_code_and_expiration()
        if self.http_response:
            return
        self.generate_response()
