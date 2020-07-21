from apis.models import User
from common.base_resource import BasePostResource
from models.order import Order
from repositories.v11.merchant_repo import MerchantRepository


class DeleteUser(BasePostResource):
    version = 10
    end_point = 'delete_user'

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        self.buyer_id = None
        self.merchant_id = None
        if self.current_user_info.get('buyer_id'):
            self.buyer_id = self.current_user_info.get('buyer_id')
        else:
            self.merchant_id = self.current_user_info.get('merchant_id')

    def verify_user_orders(self):
        """
        Verifies that either user has running orders or not
        """
        orders = Order.verify_user_orders(self.buyer_id, self.merchant_id)
        if orders:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.USER_DELETION_ORDERS_MESSAGE
            }

    def delete_user(self):
        """
        Deletes user from the system

        1. It deletes all the items and ingredients (merchant)
        2. It deletes all the reports (merchant)
        3. It deletes all the orders and orders details
        """
        User.delete_user(self.user_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_user_deleted': True
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.verify_user_orders()
        if self.is_send_response:
            return
        self.delete_user()
        self.prepare_response()
