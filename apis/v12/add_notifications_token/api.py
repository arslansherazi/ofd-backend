from apis.v12.add_notifications_token.validator import \
    AddNotificationsTokenValidator
from common.base_resource import BasePostResource
from models.notifications_token import NotificationsToken


class AddNotificationsToken(BasePostResource):
    version = 12
    end_point = 'add_notifications_token'
    request_validator = AddNotificationsTokenValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.notifications_token = self.request_args.get('notifications_token')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')

    def save_notifications_token(self):
        """
        Save expo push notifications token into db. It also verifies the duplicate token
        """
        is_token_exists = NotificationsToken.verify_duplicate_token(self.buyer_id, self.notifications_token)
        if not is_token_exists:
            NotificationsToken.save_notifications_token(self.buyer_id, self.notifications_token)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_notifications_token_saved': True
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.save_notifications_token()
        self.prepare_response()
