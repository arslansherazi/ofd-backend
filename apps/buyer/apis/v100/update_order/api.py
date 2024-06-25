from apps.buyer.apis.v100.update_order.validator import UpdateOrderValidator
from apps.buyer.models.v100.order import Order
from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class UpdateOrder(BasePostResource):
    version = 100
    end_point = 'update_order'
    request_validator = UpdateOrderValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')
        self.delivery_address = self.request_args.get('delivery_address')
        self.is_delivery = self.request_args.get('is_delivery')
        self.is_takeaway = self.request_args.get('is_takeaway')
        self.order_items = self.request_args.get('order_items')
        if self.delivery_address:
            self.latitude = self.request_args.get('latitude')
            self.longitude = self.request_args.get('longitude')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')
        self.order_new_price = 0
        self.order_new_discounted_price = 0
        self.discount = 0

    def verify_order(self):
        """
        Verifies that either order exists or not against the buyer. It also verifies that either order can be updated
        or not
        """
        order_status = Order.get_order_status(order_id=self.order_id, buyer_id=self.buyer_id)
        if not order_status:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }
        else:
            update_order = Order.verify_update_order(self.order_id)
            if not update_order:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': BuyerRepository.UPDATE_ORDER_ERROR_MESSAGE
                }

    def update_order(self):
        """
        Updates order
        """
        if self.order_items:
            BuyerRepository.update_order(
                self.order_id, self.order_items, self.delivery_address, self.latitude, self.longitude, self.is_delivery,
                self.is_takeaway
            )

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': BuyerRepository.UPDATE_ORDER_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_order()
        self.verify_order()
        if self.is_send_response:
            return
        self.update_order()
        self.prepare_response()
