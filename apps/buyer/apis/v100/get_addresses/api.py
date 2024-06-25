from apps.buyer.models.v100.address import Address
from common.base_resource import BasePostResource


class GetAddresses(BasePostResource):
    version = 100
    end_point = 'get_addresses'

    def initialize_class_attributes(self):
        """
        Intializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')
        self.addresses = []

    def get_addresses(self):
        """
        Gets addresses list
        """
        self.addresses = Address.get_addresses(self.buyer_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'addresses': self.addresses
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.get_addresses()
        self.prepare_response()
