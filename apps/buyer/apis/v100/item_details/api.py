from apps.buyer.apis.v100.item_details.validator import \
    MenuItemDetailsValidator
from apps.merchant.models.v100.ingredient import Ingredient
from common.base_resource import BasePostResource


class MenuItemDetails(BasePostResource):
    version = 100
    end_point = 'item_details'
    request_validator = MenuItemDetailsValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_item_id = self.request_args.get('menu_item_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')

    def get_menu_item_details(self):
        """
        Gets menu item details
        """
        self.menu_item_details = Ingredient.get_items_data(item_id=self.menu_item_id, user_id=self.user_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'item_details': self.menu_item_details
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_menu_item_details()
        self.prepare_response()
