from apis.v12.order_status.validator import OrderStatusValidator
from common.base_resource import BasePostResource
from models.order import Order
from repositories.v11.merchant_repo import MerchantRepository


class OrderStatus(BasePostResource):
    version = 12
    end_point = 'order_status'
    request_validator = OrderStatusValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')

    def get_order_status(self):
        """
        Gets order status. It also verifies that either order exist or not
        """
        self.order_status = Order.get_order_status(order_id=self.order_id, buyer_id=self.buyer_id)
        if not self.order_status:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'status': self.order_status
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_order_status()
        if self.is_send_response:
            return
        self.prepare_response()
