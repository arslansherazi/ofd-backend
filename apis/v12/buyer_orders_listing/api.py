from common.base_resource import BaseGetResource
from common.constants import ASSETS_BASE_URL
from models.order import Order
from repositories.v12.buyer_repo import BuyerRepository


class BuyerOrdersListing(BaseGetResource):
    version = 12
    end_point = 'buyer_orders_listing'

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.orders_history_exists = False
        self.buyer_id = self.current_user_info.get('buyer_id')

    def get_orders(self):
        """
        Gets orders
        """
        self.orders = Order.get_buyer_orders(self.buyer_id)
        if self.orders:
            self.orders_history_exists = True

    def prepare_response(self):
        """
        Prepares response
        """
        if self.orders_history_exists:
            self.response = {
                'data': {
                    'orders': self.orders
                }
            }
        else:
            self.status_code = 422
            self.response = {
                'title': BuyerRepository.NO_ORDER_TITLE,
                'message': BuyerRepository.NO_ORDER_MESSAGE,
                'image_url': '{assets_base_url}images/{image_name}'.format(
                    assets_base_url=ASSETS_BASE_URL, image_name=BuyerRepository.NO_ORDERS_IMAGE_NAME
                )
            }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.get_orders()
        self.prepare_response()
