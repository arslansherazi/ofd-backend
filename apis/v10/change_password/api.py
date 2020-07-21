from django.contrib.auth.hashers import check_password
from django.utils import timezone

from apis.models import User
from apis.v10.change_password.validator import ChangePasswordValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import LINK_EXPIRED_MESSAGE
from repositories.v10.user_repo import UserRepository


class ChangePassword(BasePostResource):
    version = 10
    end_point = 'change_password'
    request_validator = ChangePasswordValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.is_forgot_password = bool(self.request_args.get('is_forgot_password'))
        self.new_password = self.request_args.get('new_password')
        if self.is_forgot_password:
            self.encrypted_change_password_token = self.request_args.get('__c_p_t')
            self.encrypted_user_id = self.request_args.get('__ui')
        else:
            self.old_password = self.request_args.get('old_password')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.is_old_password_invalid = False
        if not self.is_forgot_password:
            self.user_id = self.current_user_info.get('user_id')

    def verify_old_password(self):
        """
        Verifies that either old password is correct or not
        """
        self.user = User.get_user_login_info(self.user_id)
        password_hash = self.user.get('password')
        if check_password(self.old_password, password_hash):
            return True
        return False

    def update_password(self):
        """
        Updates password hash
        """
        User.update_password(self.user_id, self.new_password, self.is_forgot_password)

    def process_update_password(self):
        """
        Process password updation
        If user required new password by forgot password then old password verification is not required. But old
        password verification is required for new password if user required it using app settings
        """
        if self.is_forgot_password:
            self.user_id = int(CommonHelpers.decrypt_data(self.encrypted_user_id))
            change_password_token = CommonHelpers.decrypt_data(self.encrypted_change_password_token)
            forgot_password_data = User.get_forgot_password_email_code_and_expiration(
                self.user_id, change_password_token
            )
            self.is_send_response = True
            if forgot_password_data:
                forgot_password_code_expiration = forgot_password_data.get('forgot_password_code_expiration')
                if not forgot_password_code_expiration > timezone.now():
                    self.status_code = 200
                    self.response = {
                        'message': LINK_EXPIRED_MESSAGE
                    }
                else:
                    self.update_password()
                    self.status_code = 200
                    self.response = {
                        'message': UserRepository.PASSWORD_UPDATE_SUCCESS_MESSAGE
                    }
            else:
                self.status_code = 200
                self.response = {
                    'message': LINK_EXPIRED_MESSAGE
                }
        else:
            is_password_verified = self.verify_old_password()
            if not is_password_verified:
                self.is_old_password_invalid = True
            else:
                self.update_password()

    def prepare_response(self):
        """
        Prepares response
        """
        if self.is_old_password_invalid:
            self.status_code = 403
            self.response = {
                'message': UserRepository.INVALID_PASSWORD_MESSAGE,
                'is_password_updated': False
            }
        else:
            self.response = {
                'data': {
                    'message': UserRepository.PASSWORD_UPDATE_SUCCESS_MESSAGE,
                    'is_password_updated': True
                }
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.process_update_password()
        if self.is_send_response:
            return
        self.prepare_response()
