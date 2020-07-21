from apis.v12.feedback.validator import FeedbackValidator
from common.base_resource import BasePostResource
from models.menu_item import MenuItem
from models.order_details import OrderDetails
from models.review import Review
from repositories.v12.buyer_repo import BuyerRepository


class Feedback(BasePostResource):
    version = 12
    end_point = 'feedback'
    request_validator = FeedbackValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')
        self.feedbacks = self.request_args.get('feedbacks')

    def initialize_class_arguments(self):
        """
        Initializes class arguments
        """
        self.buyer_id = self.current_user_info.get('buyer_id')

    def verify_order_items(self):
        """
        Verifies that either buyer has order against the items for which buyer is giving feedback
        """
        items_ids = list(self.feedbacks.keys())
        order_items = OrderDetails.verify_buyer_order_items(self.buyer_id, self.order_id, items_ids)
        if not order_items:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': BuyerRepository.FEEDBACK_ERROR_MESSAGE
            }

    def update_feedback(self):
        """
        Updates user feedback

        1. Updated ratings of order items
        2. Updates reviews of order items
        """
        ratings = {}
        reviews = {}
        for item_id, feedback in self.feedbacks.items():
            ratings[item_id] = feedback.get('rating')
            if feedback.get('review'):
                reviews[item_id] = feedback.get('review')
        MenuItem.save_rating(ratings)
        Review.save_review(self.buyer_id, reviews)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': BuyerRepository.FEEDBACK_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_arguments()
        self.verify_order_items()
        if self.is_send_response:
            return
        self.update_feedback()
        self.prepare_response()
