from apps.buyer.apis.v100.order_status.validator import OrderStatusValidator
from apps.buyer.models.v100.order import Order
from apps.merchant.models.v100.driver import Driver
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class OrderStatus(BasePostResource):
    version = 100
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
        if self.order_status == MerchantRepository.ON_ROUTE_ORDER_STATUS:
            self.response['data']['driver_info'] = Driver.get_driver_info(self.order_id)

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
