from apis.v12.merchants.validator import MerchantsValidator
from common.base_resource import BasePostResource
from models.merchant import Merchant


class Merchants(BasePostResource):
    version = 12
    end_point = 'merchants'
    request_validator = MerchantsValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.location_id = self.request_args.get('location_id')
        self.is_delivery = self.request_args.get('is_delivery')
        self.is_takeaway = self.request_args.get('is_takeaway')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchants = []

    def get_merchants_data(self):
        """
        Gets merchants_data
        """
        self.merchants = Merchant.get_merchants_data(self.location_id, self.is_delivery, self.is_takeaway)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'merchants': self.merchants
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_merchants_data()
        self.prepare_response()
