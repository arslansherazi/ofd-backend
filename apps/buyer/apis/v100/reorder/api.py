from apps.buyer.apis.v100.reorder.validator import ReorderValidator
from apps.buyer.models.v100.order import Order
from apps.buyer.models.v100.order_details import OrderDetails
from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from apps.merchant.models.v100.merchant import Merchant
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers


class Reorder(BasePostResource):
    version = 100
    end_point = 'reorder'
    request_validator = ReorderValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')
        self.is_price_checked = self.request_args.get('is_price_checked')
        if not self.is_price_checked:
            self.is_price_changed = self.request_args.get('is_price_changed')
            self.is_changed = self.request_args.get('is_changed')
            self.items_details = self.request_args.get('items_details')
            self.is_delivery = self.request_args.get('is_delivery')
            self.is_takeaway = self.request_args.get('is_takeaway')
            self.delivery_address = self.request_args.get('delivery_address')
            self.latitude = self.request_args.get('latitude')
            self.longitude = self.request_args.get('longitude')
        else:
            self.merchant_id = self.request_args.get('merchant_id')
            self.merchant_name = self.request_args.get('merchant_name')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')

    def verify_order(self):
        """
        Verifies that either order exists against the buyer or not
        """
        order_status = Order.get_order_status(order_id=self.order_id, buyer_id=self.buyer_id)
        if not order_status:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }

    def verify_merchant(self):
        """
        Verifies that either merchant still exists in the system or left from the company. It also verifies the
        availability of merchant
        """
        merchant = Merchant.verify_merchant_existance(self.merchant_id)
        if not merchant:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MERCHANT_NOT_EXISTS_MESSAGE.format(self.merchant_name)
            }
        else:
            merchant_availability = MerchantRepository.verify_merchant_availability(self.merchant_id)
            if not merchant_availability.get('is_merchant_online'):
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': merchant_availability.get('message')
                }

    def process_order_price_change(self):
        """
        Checks that either merchant deletes some items or changes prices of some items in the order or not.

        1. If merchant changes the prices of items or deletes some items then sends items with updated data
        2. If merchant does not delete any item or change prices of items then sends items with previous data
        """
        order = Order.get_order_data(self.order_id)
        order_items_details = OrderDetails.get_order_items_details(self.order_id)
        is_price_changed = order.get('is_price_changed')
        self.is_send_response = True
        self.response = {
            'data': {
                'is_delivery_changed': False,
                'is_takeaway_changed': False,
                'is_price_changed': is_price_changed,
                'items_details': order_items_details,
                'merchant_details': {
                    'id': order.get('merchant_id'),
                    'name': order.get('merchant_name'),
                    'address': order.get('merchant_address'),
                    'contact_no': order.get('merchant_contact_no'),
                    'location_id': order.get('merchant_location_id'),
                    'image_url': order.get('merchant_image_url'),
                    'is_delivery': order.get('is_delivery_enabled'),
                    'is_takeaway_and_delivery': order.get('is_delivery_enabled') and order.get('is_takeaway_enabled')
                },
                'delivery_details': {
                    'is_delivery': order.get('is_delivery')
                }
            }
        }
        if order.get('is_delivery'):
            self.response['data']['delivery_details']['delivery_address'] = order.get('delivery_address')
            self.response['data']['delivery_details']['average_delivery_time'] = CommonHelpers.calculate_delivery_time_and_distance(  # noqa: 501
                latitude=order.get('latitude'), longitude=order.get('longitude'),
                merchant_latitude=order.get('merchant_latitude'), merchant_longitude=order.get('merchant_longitude'),
                is_delivery=True
            )
        else:
            self.response['data']['delivery_details']['merchant_distance'] = CommonHelpers.calculate_delivery_time_and_distance(  # noqa: 501
                latitude=order.get('latitude'), longitude=order.get('longitude'),
                merchant_latitude=order.get('merchant_latitude'), merchant_longitude=order.get('merchant_longitude')
            )
        if is_price_changed:
            self.response['data']['message'] = BuyerRepository.REORDER_PRICE_CHANGE_MESSAGE.format(self.merchant_name)
        if order.get('is_delivery') and not order.get('is_delivery_enabled'):
            self.response['data']['is_delivery_changed'] = True
        if not order.get('is_delivery') and not order.get('is_takeaway_enabled'):
            self.response['data']['is_takeaway_changed'] = True

    def place_order(self):
        """
        Places order
        """
        if any([self.is_price_changed, self.is_changed]):
            BuyerRepository.update_order(
                self.order_id, self.items_details, self.delivery_address, self.latitude, self.longitude,
                self.is_delivery, self.is_takeaway
            )
            if self.is_price_changed:
                Order.update_orders_price_changed_flag([self.order_id])
        self.order_number = Order.update_order_status(self.order_id, MerchantRepository.PlACED_ORDER_STATUS)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_reordered': True,
                'order_id': self.order_id,
                'order_number': self.order_number
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_order()
        if self.is_send_response:
            return
        if self.is_price_checked:
            self.verify_merchant()
            if self.is_send_response:
                return
            self.process_order_price_change()
            if self.is_send_response:
                return
        self.place_order()
        self.prepare_response()
