import random

from apis.v12.item_details.validator import MenuItemDetailsValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import DEFAULT_ITEMS_LIMIT
from models.favourite import Favourite
from models.ingredient import Ingredient


class MenuItemDetails(BasePostResource):
    version = 12
    end_point = 'item_details'
    request_validator = MenuItemDetailsValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_item_id = int(self.request_args.get('menu_item_id'))
        self.menu_id = int(self.request_args.get('menu_id'))
        self.merchant_id = int(self.request_args.get('merchant_id'))

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        self.is_favourite = False

    def check_favourite(self):
        """
        Checks that either menu item is marked favourite or not
        """
        self.is_favourite = Favourite.verify_favourite(self.user_id, self.menu_item_id)

    def get_menu_items(self):
        """
        Gets menu items
        """
        self.menu_items = Ingredient.get_items_data(
            menu_id=self.menu_id, merchant_id=self.merchant_id, is_menu_items=True, is_buyer=True,
            user_id=self.user_id
        )

    def prepare_related_menu_items(self):
        """
        Prepares related menu items for buyer
        """
        if not len(self.menu_items) <= DEFAULT_ITEMS_LIMIT:
            related_menu_items = {}
            while True:
                related_menu_item = random.choice(self.menu_items)
                related_menu_item_id = related_menu_item.get('id')
                if related_menu_item_id not in related_menu_items:
                    related_menu_items[related_menu_item_id] = related_menu_item
                if len(list(related_menu_items.values())) >= DEFAULT_ITEMS_LIMIT:
                    break
            related_menu_items = list(related_menu_items.values())
            self.menu_items = CommonHelpers.sort_list_data(related_menu_items, key='discount', descending=True)
        else:
            self.menu_items = CommonHelpers.sort_list_data(self.menu_items, key='discount', descending=True)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'menu_items': self.menu_items,
                'is_favourite': self.is_favourite
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.check_favourite()
        self.get_menu_items()
        self.prepare_related_menu_items()
        self.prepare_response()
