from apis.v12.favourites_listing.validator import FavouritesListingValidator
from common.base_resource import BasePostResource
from common.constants import ASSETS_BASE_URL
from models.favourite import Favourite
from models.ingredient import Ingredient
from repositories.v12.buyer_repo import BuyerRepository


class FavouritesListing(BasePostResource):
    version = 12
    end_point = 'favourites_listing'
    request_validator = FavouritesListingValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.latitude = self.request_args.get('latitude')
        self.longitude = self.request_args.get('longitude')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        self.favourites = []

    def verify_favourites_count(self):
        """
        It verifies that either user add any favourite yet
        """
        favourites_count = Favourite.get_favourites_count(self.user_id)
        if favourites_count == BuyerRepository.NO_FAVOURITES_COUNT:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'title': BuyerRepository.NO_FAVOURITES_TITLE,
                'message': BuyerRepository.NO_FAVOURITES_MESSAGE,
                'image_url': '{assets_base_url}images/{image_name}'.format(
                    assets_base_url=ASSETS_BASE_URL, image_name=BuyerRepository.NO_FAVOURITES_IMAGE_NAME
                )
            }

    def get_favourites(self):
        """
        Gets favourites from db
        """
        favourites_menu_items_ids = Favourite.get_favourite_menu_items_ids(self.user_id)
        self.favourites = Ingredient.get_items_data(menu_items_ids=favourites_menu_items_ids, user_id=self.user_id)
        self.favourites = BuyerRepository.calculate_distance_btw_buyer_and_merchant(
            self.latitude, self.longitude, self.favourites, is_takeaway=True, is_delivery=True
        )

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'favourites': self.favourites
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_favourites_count()
        if self.is_send_response:
            return
        self.get_favourites()
        self.prepare_response()
