from apis.v12.add_favourite.validator import AddFavouriteValidator
from common.base_resource import BasePostResource
from models.favourite import Favourite
from repositories.v12.buyer_repo import BuyerRepository


class AddFavourite(BasePostResource):
    version = 12
    end_point = 'add_favourite'
    request_validator = AddFavouriteValidator()

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

    def verify_favourites_count(self):
        """
        Verifies that either user exceeds favourites limit or not. It also verifies that either user add any favourite
        yet
        """
        favourites_count = Favourite.get_favourites_count(self.user_id)
        if favourites_count >= BuyerRepository.FAVOURITES_LIMIT:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': BuyerRepository.FAVOURITES_LIMIT_EXCEEDS_MESSAGE
            }

    def add_favourite(self):
        """
        Adds favourite menu item into db
        """
        Favourite.insert_favourite_into_db(self.user_id, self.menu_item_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_favourite_added': True
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
        self.add_favourite()
        self.prepare_response()
