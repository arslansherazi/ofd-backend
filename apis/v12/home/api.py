from apis.v12.home.validator import HomeValidator
from common.base_resource import BasePostResource
from repositories.v12.buyer_repo import BuyerRepository


class Home(BasePostResource):
    version = 12
    end_point = 'home'
    request_validator = HomeValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')
        self.location_id = self.request_args.get('location_id')
        self.is_takeaway = self.request_args.get('is_takeaway')
        self.is_delivery = self.request_args.get('is_delivery')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.home_sections = []
        self.user_id = self.current_user_info.get('user_id')
        self.buyer_id = self.current_user_info.get('buyer_id')

    def set_discounted_section(self):
        """
        Sets discounted item home section
        """
        discounted_items_ids, discounted_items = BuyerRepository.get_discounted_items(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
            user_id=self.user_id, return_ids=True, latitude=self.latitude, longitude=self.longitude,
            distinct_results=True
        )
        if discounted_items:
            discounted_section = {
                'name': BuyerRepository.DISCOUNTED_SECTION_NAME,
                'items': discounted_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            view_all_section = BuyerRepository.set_view_all_section(discounted_items_ids)
            discounted_section['items'].append(view_all_section)
            self.home_sections.append(discounted_section)

    def set_top_rated_section(self):
        """
        Sets top rates items home section
        """
        rated_items_ids, rated_items = BuyerRepository.get_top_rated_items(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
            user_id=self.user_id, return_ids=True, latitude=self.latitude, longitude=self.longitude,
            distinct_results=True
        )
        if rated_items:
            top_rated_section = {
                'name': BuyerRepository.TOP_RATED_SECTION_NAME,
                'items': rated_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            view_all_section = BuyerRepository.set_view_all_section(rated_items_ids)
            top_rated_section['items'].append(view_all_section)
            self.home_sections.append(top_rated_section)

    def set_nearby_section(self):
        """
        Sets nearby section
        """
        nearby_items_ids, nearby_items = BuyerRepository.get_nearby_items(
            location_id=self.location_id, is_takeaway=self.is_takeaway, is_delivery=self.is_delivery,
            user_id=self.user_id, return_ids=True, latitude=self.latitude, longitude=self.longitude,
            distinct_results=True
        )
        if nearby_items:
            nearby_section = {
                'name': BuyerRepository.NEARBY_SECTION_NAME,
                'items': nearby_items[:BuyerRepository.HOME_SECTIONS_ITEMS_LIMIT]
            }
            view_all_section = BuyerRepository.set_view_all_section(nearby_items_ids)
            nearby_section['items'].append(view_all_section)
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
