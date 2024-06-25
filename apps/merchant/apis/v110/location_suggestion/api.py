import json

import requests

from apps.merchant.apis.v110.location_suggestion.validator import LocationSuggestionValidator
from common.base_resource import BasePostResource
from common.constants import GOOGLE_AUTO_COMPLETE_API_URL


class LocationSuggestions(BasePostResource):
    version = 110
    end_point = 'location_suggestions'
    request_validator = LocationSuggestionValidator()

    def populate_request_arguments(self):
        """
        Initializes class attributes
        """
        self.query = self.request_args.get('query')
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')
        self.radius = self.request_args.get('radius')

    def initialize_class_attributes(self):
        """
        Initializes class arguments
        """
        self.suggestions = []

    def get_suggestions(self):
        """
        Gets report data
        """
        auto_suggest_api_url = GOOGLE_AUTO_COMPLETE_API_URL.format(
            input=self.query, location='{latitude},{longitude}'.format(latitude=self.latitude, longitude=self.longitude),
            radius=self.radius
        )
        response = requests.get(auto_suggest_api_url)
        suggestions_data = json.loads(response.content).get('predictions', {})
        for suggestion_data in suggestions_data:
            suggestion = {
                'id': suggestion_data.get('place_id'),
                'location_primary': suggestion_data.get('description'),
                'location_secondary': suggestion_data.get('structured_formatting', {}).get('secondary_text')
            }
            self.suggestions.append(suggestion)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'suggestions': self.suggestions
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
