from common.base_resource import BasePostResource
from models.order_details import OrderDetails
from repositories.v12.buyer_repo import BuyerRepository


class BuyerOrdersListing(BasePostResource):
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
        self.orders = OrderDetails.get_buyer_orders(self.buyer_id)
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
                'image_url': BuyerRepository.NO_ORDERS_IMAGE_URL
            }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.get_orders()
        self.prepare_response()
