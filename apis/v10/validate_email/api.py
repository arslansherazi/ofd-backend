from apis.models import User
from apis.v10.validate_email.validator import ValidateEmailValidator
from common.base_resource import BasePostResource
from repositories.v10.user_repo import UserRepository


class ValidateEmail(BasePostResource):
    version = 10
    end_point = 'validate_email'
    request_validator = ValidateEmailValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.email = self.request_args.get('email')
        self.user_type = self.request_args.get('user_type')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_exists = False

    def validate_email(self):
        """
        Checks either email already exist in system or not
        """
        self.user_exists = User.check_email_availability(self.email, self.user_type)

    def prepare_response(self):
        """
        Prepares response
        """
        if not self.user_exists:
            self.response = {
                'data': {
                    'user_exists': False,
                    'message': UserRepository.EMAIL_NOT_EXISTS_MESSAGE.format(self.email)
                }
            }
        else:
            self.response = {
                'data': {
                    'user_exists': True
                }
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.validate_email()
        self.prepare_response()
