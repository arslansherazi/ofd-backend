from apis.v12.get_feedbacks.validator import FeedbacksValidator
from common.base_resource import BasePostResource
from models.feedback import Feedback


class GetFeedbacks(BasePostResource):
    version = 12
    end_point = 'get_feedbacks'
    request_validator = FeedbacksValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.item_id = self.request_args.get('item_id')

    def initialize_class_arguments(self):
        """
        Initializes class arguments
        """
        self.feedbacks = []

    def get_feedbacks(self):
        """
        Gets feedbacks
        """
        self.feedbacks = Feedback.get_feedbacks(self.item_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'feedbacks': self.feedbacks
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_arguments()
        self.get_feedbacks()
        self.prepare_response()
