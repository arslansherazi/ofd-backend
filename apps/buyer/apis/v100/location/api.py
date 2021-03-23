from geopy import Nominatim

from apps.buyer.apis.v100.location.validator import VerifyLocationValidator
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers


class VerifyLocation(BasePostResource):
    version = 100
    end_point = 'verify_location'
    request_validator = VerifyLocationValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.location_id = self.request_args.get('location_id')
        self.address = self.request_args.get('address')

    def initialize_class_attributes(self):
        """
        initializes class attributes
        """
        self.geolocator = Nominatim(user_agent='ofd')
        self.location = None
        self.location_latitude = 0.0
        self.location_longitude = 0.0

    def verify_address(self):
        """
        Verifies that either address is valid or not
        """
        location = self.geolocator.geocode(self.address)
        self.location_latitude = location.latitude
        self.location_longitude = location.longitude
        if not all([self.location_latitude, self.location_longitude]):
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.INVALID_ADDRESS_MESSAGE
            }

    def verify_location(self):
        """
        Verifies that either address lies within the location or not
        """
        location_id = CommonHelpers.get_location_id(self.location_latitude, self.location_longitude)
        if location_id != self.location_id:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.INVALID_LOCATION_ADDRESS_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'latitude': self.location_latitude,
                'longitude': self.location_longitude
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
        self.verify_location()
        if self.is_send_response:
            return
        self.prepare_response()
