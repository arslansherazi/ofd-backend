from apps.buyer.models.v100.order_details import OrderDetails
from apps.merchant.apis.v100.delete_menu.validator import DeleteMenuValidator
from apps.merchant.models.v100.ingredient import Ingredient
from apps.merchant.models.v100.menu import Menu
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class DeleteMenu(BasePostResource):
    version = 100
    end_point = 'delete_menu'
    request_validator = DeleteMenuValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_id = self.request_args.get('menu_id')

    def initialize_class_arguments(self):
        """
        Initializes class arguments
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.is_menu_deleted = False
        self.is_menu_contains_orders = False

    def verify_menu(self):
        """
        Verifies either menu exists or not against the merchants
        """
        is_menu_exists = Menu.verify_menu(self.menu_id, self.merchant_id)
        if not is_menu_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_NOT_EXIST_MESSAGE
            }

    def verify_menu_items(self):
        """
        Verifies that either items exists in the menu or not. If there is no item in the menu then delete it
        """
        menu_items = Ingredient.get_items_data(
            menu_id=self.menu_id, merchant_id=self.merchant_id, is_menu_items=True
        )
        if not menu_items:
            Menu.delete_menu(self.menu_id)
            self.is_menu_deleted = True
        else:
            self.verify_menu_items_orders()

    def verify_menu_items_orders(self):
        """
        Verifies that either running orders exist against items in the menu. If no order exist then delete the menu
        """
        menu_items_orders = OrderDetails.verify_menu_items_orders(self.menu_id, self.merchant_id)
        if menu_items_orders:
            self.is_menu_contains_orders = True
        else:
            Menu.delete_menu(self.menu_id)

    def prepare_response(self):
        """
        Prepares response
        """
        if self.is_menu_contains_orders:
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_CONTAINS_ORDERS_MESSAGE
            }
        else:
            self.response = {
                'message': MerchantRepository.MENU_DELETED_SUCCESSFULLY_MESSAGE
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_arguments()
        self.verify_menu()
        if self.is_send_response:
            return
        self.verify_menu_items()
        self.prepare_response()
