from apis.v11.order_details.validation import OrderDetailsValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from models.order_details import OrderDetails
from repositories.v11.merchant_repo import MerchantRepository


class OrderDetailsApi(BasePostResource):
    version = 11
    end_point = 'order_details'
    request_validator = OrderDetailsValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')
        self.merchant_id = self.request_args.get('merchant_id')
        self.buyer_id = self.request_args.get('buyer_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.buyer_order_details = False
        if self.merchant_id:
            self.buyer_order_details = True
            self.buyer_id = self.current_user_info.get('buyer_id')
        else:
            self.merchant_id = self.current_user_info.get('merchant_id')

    def get_order_details(self):
        """
        Gets order details
        """
        self.order_details_data = OrderDetails.get_order_details(
            self.order_id, self.merchant_id, self.buyer_id, self.buyer_order_details
        )
        if not self.order_details_data:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }

    def process_order_details(self):
        """
        Process order details

        1. It calculates discounted price of order if discount exists for order
        2. It calculates discounted price of all items in order if discount exists
        """
        order_details = self.order_details_data.first()
        price = order_details.get('price')
        buyer_name = order_details.get('buyer_name')
        self.order_details = {
            'order_id': order_details.get('order_id'),
            'order_number': order_details.get('order_number'),
            'status': order_details.get('status'),
            'price': price,
            'is_delivery': order_details.get('is_delivery'),
            'buyer_name': CommonHelpers.capitalize_string(buyer_name),
            'items_details': []
        }
        if order_details.get('is_delivery'):
            delivery_address = order_details.get('delivery_address')
            self.order_details.update(delivery_address=CommonHelpers.capitalize_string(delivery_address))
        if self.buyer_order_details:
            self.order_details.update(
                merchant_name=order_details.get('merchant_name'),
                merchant_contact_no=order_details.get('merchant_contact_no')
            )
        if order_details.get('discount'):
            discount = order_details.get('discount')
            self.order_details.update(
                discount='{}%'.format(discount),
                discounted_price=round(price - ((price / 100) * discount))
            )
        for order_details_data in self.order_details_data:
            price = order_details_data.get('item_price')
            item_quantity = order_details_data.get('item_quantity')
            total_price = price * item_quantity
            item_details = {
                'id': order_details_data.get('id'),
                'item_id': order_details_data.get('item_id'),
                'name': order_details_data.get('name'),
                'unit': order_details_data.get('unit'),
                'quantity': order_details_data.get('quantity'),
                'rating': order_details_data.get('rating'),
                'price': price,
                'item_quantity': item_quantity,
                'total_price': total_price
            }
            if order_details_data.get('item_discount'):
                discount = order_details.get('item_discount')
                item_details.update(
                    discount='{}%'.format(discount),
                    discounted_price=round(total_price - ((total_price / 100) * discount))
                )
            self.order_details.get('items_details').append(item_details)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'order_details': self.order_details
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_order_details()
        if self.is_send_response:
            return
        self.process_order_details()
        self.prepare_response()
