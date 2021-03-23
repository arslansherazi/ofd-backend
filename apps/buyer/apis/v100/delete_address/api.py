from apps.buyer.apis.v100.delete_address.validation import DeleteAddressValidator
from apps.buyer.models.v100.address import Address
from common.base_resource import BasePostResource


class DeleteAddress(BasePostResource):
    version = 100
    end_point = 'delete_address'
    request_validator = DeleteAddressValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.address_id = self.request_args.get('address_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')

    def verify_address(self):
        """
        verifies that either address exist against the buyer or not
        """
        is_address_exists = Address.verify_buyer_address(self.buyer_id, self.address_id)
        if not is_address_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': 'Address does not exist'
            }

    def delete_address(self):
        """
        Deletes address
        """
        Address.delete_address(self.address_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_address_deleted': True
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_address()
        if self.is_send_response:
            return
        self.delete_address()
        self.prepare_response()
