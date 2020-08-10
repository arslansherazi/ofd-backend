from apis.v12.home.validator import HomeValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from models.ingredient import Ingredient
from repositories.v12.buyer_repo import BuyerRepository


class Home(BasePostResource):
    version = 12
    end_point = 'home'
    request_validator = HomeValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.latitude = float(self.request_args.get('latitude'))
        self.longitude = float(self.request_args.get('longitude'))
        self.location_id = int(self.request_args.get('location_id'))
        self.is_takeaway = bool(int(self.request_args.get('is_takeaway')))
        self.is_delivery = bool(int(self.request_args.get('is_delivery')))

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.home_sections = []
        self.user_id = self.current_user_info.get('user_id')

    def set_discounted_section(self):
        """
        Sets discounted item home section
        """
        discounted_items = Ingredient.get_items_data(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
            is_discounted=True, user_id=self.user_id
        )
        if discounted_items:
            discounted_items = BuyerRepository.calculate_distance_btw_buyer_and_merchant(
                self.latitude, self.longitude, discounted_items, self.is_takeaway, self.is_delivery
            )
            sorted_discounted_items = CommonHelpers.sort_list_data(discounted_items, key='discount', descending=True)
            distinct_discounted_items = BuyerRepository.get_distinct_merchants_items(sorted_discounted_items)
            discounted_section = {
                'name': BuyerRepository.DISCOUNTED_SECTION_NAME,
                'items': distinct_discounted_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            self.home_sections.append(discounted_section)

    def set_top_rated_section(self):
        """
        Sets top rates items home section
        """
        rated_items = Ingredient.get_items_data(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery, is_top_rated=True,
            user_id=self.user_id
        )
        if rated_items:
            rated_items = BuyerRepository.calculate_distance_btw_buyer_and_merchant(
                self.latitude, self.longitude, rated_items, self.is_takeaway, self.is_delivery
            )
            top_rated_items = CommonHelpers.sort_list_data(rated_items, key='rating', descending=True)
            distinct_top_rated_items = BuyerRepository.get_distinct_merchants_items(top_rated_items)
            top_rated_section = {
                'name': BuyerRepository.TOP_RATED_SECTION_NAME,
                'items': distinct_top_rated_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            self.home_sections.append(top_rated_section)

    def set_nearby_section(self):
        """
        Sets nearby section
        """
        nearby_items = Ingredient.get_items_data(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
            user_id=self.user_id
        )
        if nearby_items:
            nearby_items = BuyerRepository.calculate_distance_btw_buyer_and_merchant(
                self.latitude, self.longitude, nearby_items, self.is_takeaway, self.is_delivery
            )
            if self.is_takeaway:
                sorted_nearby_items = CommonHelpers.sort_list_data(nearby_items, key='distance')
            else:
                sorted_nearby_items = CommonHelpers.sort_list_data(nearby_items, key='delivery_time')
            distinct_nearby_items = BuyerRepository.get_distinct_merchants_items(sorted_nearby_items)
            nearby_section = {
                'name': BuyerRepository.NEARBY_SECTION_NAME,
                'items': distinct_nearby_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            self.home_sections.append(nearby_section)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'home_sections': self.home_sections
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.set_discounted_section()
        self.set_top_rated_section()
        self.set_nearby_section()
        self.prepare_response()
