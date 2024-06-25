import json

import requests

from apps.merchant.apis.v110.get_location_by_latlng.validator import GetLocationBylatLngValidator
from common.base_resource import BasePostResource
from common.constants import GOOGLE_GEOCODE_API_URL


class GetLocationByLatLng(BasePostResource):
    version = 110
    end_point = 'get_location_by_latlng'
    request_validator = GetLocationBylatLngValidator()

    def populate_request_arguments(self):
        """
        Initializes class attributes
        """
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')

    def initialize_class_attributes(self):
        """
        Initializes class arguments
        """
        self.address = ''

    def get_suggestions(self):
        """
        Gets report data
        """
        place_details_api_url = GOOGLE_GEOCODE_API_URL.format(latlng='{lat},{lng}'.format(lat=self.latitude, lng=self.longitude))
        response = requests.get(place_details_api_url)
        location_details = json.loads(response.content).get('results', [])
        if location_details:
            self.address = location_details[0].get('formatted_address')

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'address': self.address
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
