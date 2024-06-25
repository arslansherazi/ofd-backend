from apps.buyer.apis.v100.feedback.validator import FeedbackValidator
from apps.buyer.models.v100.feedback import Feedback
from apps.buyer.models.v100.order import Order
from apps.buyer.models.v100.order_details import OrderDetails
from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from apps.merchant.models.v100.menu_item import MenuItem
from common.base_resource import BasePostResource


class FeedbackApi(BasePostResource):
    version = 100
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
        items_ids = [int(item_id) for item_id in self.feedbacks.keys()]
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
        for item_id, feedback in self.feedbacks.items():
            ratings[int(item_id)] = feedback.get('rating')
        MenuItem.save_rating(ratings)
        Feedback.save_feedback(self.buyer_id, self.feedbacks)
        Order.change_review_flag(self.order_id, is_reviewed=True)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'message': BuyerRepository.FEEDBACK_SUCCESS_MESSAGE
            }
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
