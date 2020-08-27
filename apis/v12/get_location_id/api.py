from apis.v12.get_location_id.validator import GetLocationIdValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from repositories.v12.buyer_repo import BuyerRepository


class GetLocationId(BasePostResource):
    version = 12
    end_point = 'get_location_id'
    request_validator = GetLocationIdValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')

    def verify_location(self):
        """
        Verifies that either user in the working locations of app or not
        """
        self.location_id = CommonHelpers.get_location_id(self.latitude, self.longitude)
        if not self.location_id:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'out_of_reach_title': BuyerRepository.OUT_OF_REACH_TITLE,
                'out_of_reach_message': BuyerRepository.OUT_OF_REACH_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'location_id': self.location_id
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.verify_location()
        if self.is_send_response:
            return
        self.prepare_response()
