import requests

from apis.v12.make_tiny_url.validator import MakeTinyUrlValidator
from common.base_resource import BasePostResource


class MakeTinyUrl(BasePostResource):
    version = 12
    end_point = 'make_tiny_url'
    request_validator = MakeTinyUrlValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.url = self.request_args.get('url')

    def initialize_class_arguments(self):
        """
        Initializes class arguments
        """
        self.tiny_url = ''

    def get_tiny_url(self):
        """
        Gets tiny url
        """
        response = requests.get('http://tinyurl.com/api-create.php?url={}'.format(self.url))
        self.tiny_url = response.text

    def generate_response(self):
        """
        Generates response
        """
        self.response = {
            'data': {
                'tiny_url': self.tiny_url
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_arguments()
        self.get_tiny_url()
        self.generate_response()
