from apis.v12.view_all_items.validation import ViewAllItemsValidator
from common.base_resource import BasePostResource
from models.ingredient import Ingredient
from repositories.v12.buyer_repo import BuyerRepository


class ViewAllItems(BasePostResource):
    version = 12
    end_point = 'view_all_items'
    request_validator = ViewAllItemsValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.is_merchant = self.request_args.get('is_merchant')
        self.limit = self.request_args.get('limit')
        self.offset = self.request_args.get('offset')
        self.is_discounted = self.request_args.get('is_discounted')
        self.is_top_rated = self.request_args.get('is_top_rated')
        self.is_nearby = self.request_args.get('is_nearby')
        if not self.is_merchant:
            self.latitude = self.request_args.get('latitude')
            self.longitude = self.request_args.get('longitude')
            self.location_id = self.request_args.get('location_id')
            self.is_takeaway = self.request_args.get('is_takeaway')
            self.is_delivery = self.request_args.get('is_delivery')
        else:
            self.merchant_id = self.request_args.get('merchant_id')
            self.menu_id = self.request_args.get('menu_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.items = []
        self.user_id = self.current_user_info.get('user_id')

    def get_discounted_items(self):
        """
        Gets discounted items
        """
        self.items = BuyerRepository.get_discounted_items(
            location_id=self.location_id, latitude=self.latitude, longitude=self.longitude, user_id=self.user_id,
            is_delivery=self.is_delivery, is_takeaway=self.is_takeaway
        )
        self.items = self.items[self.offset:self.offset + self.limit]

    def get_top_rated_items(self):
        """
        Gets top rated items
        """
        self.items = BuyerRepository.get_top_rated_items(
            location_id=self.location_id, latitude=self.latitude, longitude=self.longitude, user_id=self.user_id,
            is_delivery=self.is_delivery, is_takeaway=self.is_takeaway
        )
        self.items = self.items[self.offset:self.offset + self.limit]

    def get_nearby_items(self):
        """
        Gets near by items
        """
        self.items = BuyerRepository.get_nearby_items(
            location_id=self.location_id, latitude=self.latitude, longitude=self.longitude, user_id=self.user_id,
            is_delivery=self.is_delivery, is_takeaway=self.is_takeaway
        )
        self.items = self.items[self.offset:self.offset + self.limit]

    def get_related_menu_items(self):
        """
        Gets menu related items
        """
        self.items = Ingredient.get_items_data(
            menu_id=self.menu_id, merchant_id=self.merchant_id, is_menu_items=True, is_buyer=True,
            user_id=self.user_id
        )
        self.items = self.items[self.offset:self.offset + self.limit]

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'items': self.items
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        if self.is_discounted:
            self.get_discounted_items()
        if self.is_top_rated:
            self.get_top_rated_items()
        if self.is_nearby:
            self.get_nearby_items()
        if self.is_merchant:
            self.get_related_menu_items()
        self.prepare_response()
