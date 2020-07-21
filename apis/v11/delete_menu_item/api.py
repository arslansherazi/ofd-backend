from apis.v11.delete_menu_item.validator import DeleteMenuItemValidator
from common.base_resource import BasePostResource
from models.menu_item import MenuItem
from models.order_details import OrderDetails
from repositories.v11.merchant_repo import MerchantRepository


class DeleteMenuItem(BasePostResource):
    version = 11
    end_point = 'delete_menu_item'
    request_validator = DeleteMenuItemValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_item_id = self.request_args.get('menu_item_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.request_args.get('merchant_id')

    def verify_menu_item(self):
        """
        Verifies that either menu item exists against the merchant or not
        """
        menu_item = MenuItem.get_menu_item(self.menu_item_id, self.merchant_id)
        if not menu_item:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ITEM_NOT_EXIST_MESSAGE
            }

    def verify_menu_item_orders(self):
        """
        Verifies that either menu item participates in running orders or not
        """
        menu_item_orders = OrderDetails.verify_menu_item_orders(self.menu_item_id)
        if menu_item_orders:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ITEM_ORDERS_MESSAGE
            }
        else:
            MenuItem.delete_menu_item(self.menu_item_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.MENU_ITEM_DELETION_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_menu_item()
        if self.is_send_response:
            return
        self.verify_menu_item_orders()
        if self.is_send_response:
            return
        self.prepare_response()
