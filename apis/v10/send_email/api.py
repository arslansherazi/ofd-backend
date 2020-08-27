from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from apis.models import User
from apis.v10.send_email.validator import SendEmailValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import (CHANGE_PASSWORD_SUBJECT,
                              EMAIL_VERIFICATION_SUBJECT, SYSTEM_SENDER_EMAIL,
                              WEB_ROUTING_PREFIX)
from repositories.v10.user_repo import UserRepository


class SendEmail(BasePostResource):
    version = 10
    end_point = 'send_email'
    request_validator = SendEmailValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.user_type = self.request_args.get('user_type')
        self.is_forgot_password_code = self.request_args.get('is_forgot_password_code')
        self.is_email_verification_code = self.request_args.get('is_email_verification_code')
        self.is_change_email_code = self.request_args.get('is_change_email_code')
        self.email = self.request_args.get('email')
        if self.is_change_email_code:
            self.new_email = self.request_args.get('new_email')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.email_verification_link = ''
        self.user_id = User.get_user_id(self.email, self.user_type)

    def verify_duplicate_email(self):
        """
        Verifies that either email already registered or not
        """
        if self.is_change_email_code:
            is_email_already_exists = User.verify_email(self.new_email)
            if is_email_already_exists:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': UserRepository.EMAIL_ALREADY_REGISTERED_MESSAGE.format(self.new_email)
                }

    def generate_email_verification_data(self):
        """
        Generates email verification data
        """
        if self.is_email_verification_code:
            email_verification_code = CommonHelpers.generate_six_digit_random_code()
            User.update_email_verification_code_and_expiration(self.user_id, email_verification_code)
            email_verification_request = 'ofd_apis/v{api_version}/verify_email?user_id={user_id}&code={code}&is_email_verification_code=True'.format(  # noqa: 501
                api_version=self.version, user_id=self.user_id, code=email_verification_code
            )
        elif self.is_forgot_password_code:
            forgot_password_code = CommonHelpers.generate_six_digit_random_code()
            change_password_token = User.update_forgot_password_code_and_expiration(
                self.user_id, forgot_password_code
            )
            email_verification_request = 'ofd_apis/v{api_version}/verify_email?user_id={user_id}&code={code}&is_forgot_password_code=True&change_password_token={change_password_token}'.format(  # noqa: 501
                api_version=self.version, user_id=self.user_id, code=forgot_password_code,
                change_password_token=change_password_token
            )
        else:
            change_email_code = CommonHelpers.generate_six_digit_random_code()
            User.update_change_email_code_and_expiration(self.user_id, change_email_code)
            email_verification_request = 'ofd_apis/v{api_version}/verify_email?user_id={user_id}&old_email={old_email}&new_email={new_email}&code={code}&is_email_change_code=True'.format(  # noqa: 501
                api_version=self.version, user_id=self.user_id, old_email=self.email, new_email=self.new_email,
                code=change_email_code
            )
        encrypted_verification_request = CommonHelpers.encrypt_data(email_verification_request)
        self.email_verification_link = '{base_url}/{web_routing_prefix}/{encrypted_verification_request}'.format(
            base_url=settings.BASE_URL, web_routing_prefix=WEB_ROUTING_PREFIX,
            encrypted_verification_request=encrypted_verification_request
        )

    def send_email(self):
        """
        Sends email which contains verification code for email verification
        """
        if self.is_forgot_password_code:
            subject = CHANGE_PASSWORD_SUBJECT
            email_verification_text = 'Change Password'
        else:
            subject = EMAIL_VERIFICATION_SUBJECT
            email_verification_text = 'Verify Email'
        from_email = SYSTEM_SENDER_EMAIL
        to_emails = [self.email]
        email_verification_template_data = {
            'email_verification_link': self.email_verification_link,
            'email_verification_main_text': email_verification_text.lower(),
            'email_verification_button_text': email_verification_text,
        }
        html_content = render_to_string('email_verification_template.html', email_verification_template_data)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, to_emails)
        email.attach_alternative(html_content, 'text/html')
        email.send()

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_email_sent': True,
                'message': UserRepository.EMAIL_VERIFICATION_CODE_MESSAGE
            }
        }
        if self.is_change_email_code:
            self.response['data'].update(message=UserRepository.NEW_EMAIL_VERIFICATION_MESSAGE)

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_duplicate_email()
        if self.is_send_response:
            return
        self.generate_email_verification_data()
        self.send_email()
        self.prepare_response()
