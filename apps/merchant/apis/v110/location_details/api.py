import json

import requests

from apps.merchant.apis.v110.location_details.validator import LocationDetailsValidator
from common.base_resource import BasePostResource
from common.constants import GOOGLE_PLACE_DETAILS_API_URL


class LocationDetails(BasePostResource):
    version = 110
    end_point = 'location_details'
    request_validator = LocationDetailsValidator()

    def populate_request_arguments(self):
        """
        Initializes class attributes
        """
        self.place_id = self.request_args.get('place_id')

    def initialize_class_attributes(self):
        """
        Initializes class arguments
        """
        self.details = []

    def get_suggestions(self):
        """
        Gets report data
        """
        place_details_api_url = GOOGLE_PLACE_DETAILS_API_URL.format(place_id=self.place_id)
        response = requests.get(place_details_api_url)
        self.details = json.loads(response.content).get('result', {}).get('geometry', {}).get('location', {})

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'location': self.details
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_suggestions()
        self.prepare_response()
