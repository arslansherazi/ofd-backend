import uuid

from apis.v12.place_order.validation import PlaceOrderValidator
from common.base_resource import BasePostResource
from models.order import Order
from models.order_details import OrderDetails
from repositories.v11.merchant_repo import MerchantRepository
from repositories.v12.buyer_repo import BuyerRepository


class PlaceOrder(BasePostResource):
    version = 12
    end_point = 'place_order'
    request_validator = PlaceOrderValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.merchant_id = self.request_args.get('merchant_id')
        self.is_delivery = self.request_args.get('is_delivery')
        self.order_details = self.request_args.get('order_details')
        self.delivery_address = self.request_args.get('delivery_address')
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_id = self.current_user_info.get('buyer_id')
        self.price = 0
        self.discount = 0
        self.discounted_price = 0
        self.order_number = ''

    def check_duplicate_order(self):
        """
        Checks either order already exists for same merchant or not
        """
        orders_data = Order.verify_duplicate_order(self.merchant_id, self.buyer_id)
        for order_data in orders_data:
            order_status = order_data.get('status')
            if order_status in BuyerRepository.EDITABLE_ORDER_STATUSES:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'data': {
                        'is_order_placed': False,
                        'is_order_editable': True,
                        'order_id': order_data.get('id')
                    },
                    'message': BuyerRepository.DUPLICATE_ORDER_MESSAGE.format(BuyerRepository.EDITABLE_ORDER_MESSAGE)
                }

    def check_merchant_availability(self):
        """
        Verifies that either merchant is online or not
        """
        merchant_availability = MerchantRepository.verify_merchant_availability(self.merchant_id)
        if not merchant_availability.get('is_merchant_online'):
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': merchant_availability.get('message')
            }

    def process_order(self):
        """
        Process order
        """
        for order_detail in self.order_details:
            price = order_detail.get('price')
            item_quantity = order_detail.get('item_quantity')
            discount = order_detail.get('discount', 0)
            total_price = price * item_quantity
            self.price += total_price
            self.discounted_price = self.discounted_price + ((price / 100) * discount)
        self.discount = round(((self.price - (self.price - self.discounted_price)) / self.price) * 100)

    def generate_order_number(self):
        """
        Generates order number
        """
        unique_order_number = str(uuid.uuid4())
        self.order_number = unique_order_number.split('-')[0]

    def place_order(self):
        """
        Places order
        """
        self.order_id = Order.save_order(
            self.merchant_id, self.buyer_id, self.price, self.is_delivery, self.delivery_address,
            self.order_number, self.latitude, self.longitude, self.discount
        )
        OrderDetails.save_order_details(self.order_id, self.order_details)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_order_placed': True,
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
        self.check_duplicate_order()
        self.check_merchant_availability()
        if self.is_send_response:
            return
        if self.is_send_response:
            return
        self.process_order()
        self.generate_order_number()
        self.place_order()
        self.prepare_response()
