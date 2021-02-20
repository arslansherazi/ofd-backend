from fuzzywuzzy import process

from apis.v12.items_listing.validator import ItemsListingValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import (FUZZY_SCORE, FUZZY_SEARCH_RECORDS_LIMIT,
                              ITEMS_LISTING_PAGE_LIMIT)
from models.ingredient import Ingredient
from repositories.v12.buyer_repo import BuyerRepository


class ItemsListing(BasePostResource):
    version = 12
    end_point = 'items_listing'
    request_validator = ItemsListingValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.query = self.request_args.get('query')
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')
        self.is_takeaway = self.request_args.get('is_takeaway')
        self.is_delivery = self.request_args.get('is_delivery')
        self.offset = self.request_args.get('offset')
        self.is_auto_suggest_items = self.request_args.get('is_auto_suggest_items')
        self.is_auto_suggest = self.request_args.get('is_auto_suggest')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.limit = ITEMS_LISTING_PAGE_LIMIT
        self.final_outlets = []
        self.location_id = 0
        self.user_id = self.current_user_info.get('user_id')

    def get_items(self):
        """
        Gets items of location
        """
        if not self.is_auto_suggest_items:
            items = Ingredient.get_items_data(
                location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
                user_id=self.user_id
            )
            items_hash = dict()
            filtered_items = []
            for index, item in enumerate(items):
                items_hash[index] = item.get('name')
            fuzzy_outlets = process.extract(query=self.query, choices=items_hash, limit=FUZZY_SEARCH_RECORDS_LIMIT)
            if not self.is_auto_suggest:
                if fuzzy_outlets:
                    for fuzzy_outlet in fuzzy_outlets:
                        if fuzzy_outlet[1] > FUZZY_SCORE:
                            item_index = fuzzy_outlet[2]
                            item = items[item_index]
                            filtered_items.append(item)
                if not filtered_items:
                    self.generate_no_search_results_response()
                else:
                    self.get_final_items(filtered_items)
            else:
                menu_items_data = {}
                for fuzzy_outlet in fuzzy_outlets:
                    if fuzzy_outlet[1] > FUZZY_SCORE:
                        fuzzy_outlet_name = fuzzy_outlet[0]
                        if fuzzy_outlet_name in menu_items_data:
                            menu_items_data[fuzzy_outlet_name]['count'] = menu_items_data[fuzzy_outlet_name]['count'] + 1
                        else:
                            menu_items_data[fuzzy_outlet_name] = {
                                'name': fuzzy_outlet[0],
                                'count': 1
                            }
                self.is_send_response = True
                self.response = {
                    'data': {
                        'menu_items_data': list(menu_items_data.values())
                    }
                }
        else:
            items = Ingredient.get_items_data(
                location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
                user_id=self.user_id, query=self.query
            )
            if not items:
                self.generate_no_search_results_response()
            else:
                self.get_final_items(items)

    def generate_no_search_results_response(self):
        """
        Verifies that either any item exists against query or not
        """
        self.is_send_response = True
        self.status_code = 422
        self.response = {
            'title': BuyerRepository.NO_ITEMS_FOUND_TITLE,
            'message': BuyerRepository.NO_ITEMS_FOUND_MESSAGE
        }

    def get_final_items(self, items):
        """
        Gets sorted items
        """
        items = BuyerRepository.calculate_distance_btw_buyer_and_merchant(
            self.latitude, self.longitude, items, self.is_takeaway, self.is_delivery
        )
        if self.is_takeaway:
            items = CommonHelpers.sort_list_data(items, key='distance')
        else:
            items = CommonHelpers.sort_list_data(items, key='delivery_time')
        self.final_outlets = items[self.offset:self.offset + self.limit]

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'items': self.final_outlets
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_items()
        if self.is_send_response:
            return
        self.prepare_response()
