from apps.buyer.apis.v100.add_new_address.validator import AddNewAddressValidator
from apps.buyer.models.v100.address import Address
from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from common.base_resource import BasePostResource
from common.constants import BUYER_ADDRESSES_LIMIT


class AddNewAddress(BasePostResource):
    version = 100
    end_point = 'add_new_address'
    request_validator = AddNewAddressValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.building_address = self.request_args.get('building_address')
        self.street_address = self.request_args.get('street_address')
        self.state_address = self.request_args.get('state_address')
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')
        self.tag = self.request_args.get('tag')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')
        self.address_id = 0

    def verify_duplicate_address(self):
        """
        Verifies duplicate address
        """
        is_address_exists = Address.verify_address(
            self.buyer_id, self.building_address, self.street_address, self.state_address, self.tag
        )
        if is_address_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': BuyerRepository.ADDRESS_ALREADY_PRESENT_MESSAGE.format(self.tag)
            }

    def verify_addresses_limit(self):
        """
        Verifies addresses limit
        """
        addresses_count = Address.get_addresses_count(self.buyer_id)
        if addresses_count > BUYER_ADDRESSES_LIMIT:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': BuyerRepository.ADDRESS_LIMIT_EXCEEDS_MESSAGE.format(BUYER_ADDRESSES_LIMIT)
            }

    def save_address(self):
        """
        Saves address
        """
        self.address_id = Address.save_address(
            self.buyer_id, self.building_address, self.street_address, self.state_address, self.latitude,
            self.longitude, self.tag
        )

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_address_saved': True,
                'address_id': self.address_id
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_duplicate_address()
        if self.is_send_response:
            return
        self.verify_addresses_limit()
        if self.is_send_response:
            return
        self.save_address()
        self.prepare_response()
