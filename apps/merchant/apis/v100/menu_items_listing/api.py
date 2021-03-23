import random

from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from apps.merchant.apis.v100.menu_items_listing.validator import \
    MenuItemsListingValidator
from apps.merchant.models.v100.ingredient import Ingredient
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import DEFAULT_ITEMS_LIMIT


class MenuItemsListing(BasePostResource):
    version = 100
    end_point = 'menu_items_listing'
    request_validator = MenuItemsListingValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_id = self.request_args.get('menu_id')
        self.merchant_id = self.request_args.get('merchant_id')
        self.menu_item_id = self.request_args.get('menu_item_id')
        self.is_buyer = self.request_args.get('is_buyer')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        if not self.is_buyer:
            self.merchant_id = self.current_user_info.get('merchant_id')

    def get_menu_items(self):
        """
        Gets menu items
        """
        self.menu_items_ids, self.menu_items = Ingredient.get_items_data(
            menu_id=self.menu_id, merchant_id=self.merchant_id, is_menu_items=True, is_buyer=self.is_buyer,
            user_id=self.user_id, return_ids=True
        )
        if not self.is_buyer and not self.menu_items:
            self.status_code = 422
            self.is_send_response = True
            self.response = {
                'message': MerchantRepository.NO_MENU_ITEM_EXISTS_MESSAGE
            }

    def prepare_related_menu_items(self):
        """
        Prepares related menu items for buyer
        """
        if self.is_buyer:
            if not len(self.menu_items) <= DEFAULT_ITEMS_LIMIT:
                related_menu_items = {}
                while True:
                    related_menu_item = random.choice(self.menu_items)
                    related_menu_item_id = related_menu_item.get('id')
                    if related_menu_item_id not in related_menu_items and related_menu_item_id != self.menu_item_id:
                        related_menu_items[related_menu_item_id] = related_menu_item
                    if len(list(related_menu_items.values())) >= DEFAULT_ITEMS_LIMIT:
                        break
                related_menu_items = list(related_menu_items.values())
                self.menu_items = CommonHelpers.sort_list_data(related_menu_items, key='discount', descending=True)
            else:
                self.menu_items = CommonHelpers.sort_list_data(self.menu_items, key='discount', descending=True)
                for index, menu_item in enumerate(self.menu_items):
                    menu_item_id = menu_item.get('id')
                    if menu_item_id == self.menu_item_id:
                        del self.menu_items[index]
                        break
            view_all_section = BuyerRepository.set_view_all_section(self.menu_items_ids)
            self.menu_items.append(view_all_section)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'menu_items': self.menu_items
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_menu_items()
        if self.is_send_response:
            return
        self.prepare_related_menu_items()
        self.prepare_response()
