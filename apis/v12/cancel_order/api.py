from apis.v12.cancel_order.validator import CancelOrderValidator
from common.base_resource import BasePostResource
from models.order import Order
from repositories.v11.merchant_repo import MerchantRepository


class CancelOrder(BasePostResource):
    version = 12
    end_point = 'cancel_order'
    request_validator = CancelOrderValidator()

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
        self.is_order_cancelled = False

    def cancel_order(self):
        """
        Cancels order. It also verifies that either order exist or not against the buyer.
        To cancel an order status should be Placed or Accepted otherwise order cannot be cancelled
        """
        self.order_status = Order.get_order_status(order_id=self.order_id, buyer_id=self.buyer_id)
        if not self.order_status:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }
        else:
            if self.order_status in [MerchantRepository.PlACED_ORDER_STATUS, MerchantRepository.ACCEPTED_ORDER_STATUS]:
                Order.update_order_status(self.order_id, MerchantRepository.CANCELLED_ORDER_STATUS)
                self.is_order_cancelled = True

    def prepare_response(self):
        """
        Prepares response
        """
        if self.is_order_cancelled:
            self.response = {
                'message': MerchantRepository.ORDER_CANCELLATION_SUCCESS_MESSAGE
            }
        else:
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_FAILED_MESSAGE.format(
                    MerchantRepository.CANCELLED_ORDER_STATUS.lower()
                )
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.cancel_order()
        if self.is_send_response:
            return
        self.prepare_response()
