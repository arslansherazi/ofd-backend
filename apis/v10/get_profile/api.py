from apis.v10.get_profile.validator import GetProfileValidator
from common.base_resource import BasePostResource
from common.constants import BUYER_USER_TYPE
from models.buyer import Buyer
from models.merchant import Merchant


class GetProfile(BasePostResource):
    version = 10
    end_point = 'get_profile'
    request_validator = GetProfileValidator()

    def populate_request_arguments(self):
        """
        populates request arguments
        """
        self.user_type = self.request_args.get('user_type')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        if self.user_type == BUYER_USER_TYPE:
            self.buyer_id = self.current_user_info.get('buyer_id')
        else:
            self.merchant_id = self.current_user_info.get('merchant_id')

    def get_user_profile(self):
        """
        Gets user profile
        """
        if self.user_type == BUYER_USER_TYPE:
            self.profile = Buyer.get_profile(self.buyer_id)
        else:
            self.profile = Merchant.get_profile(self.merchant_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': self.profile
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_user_profile()
        self.prepare_response()
