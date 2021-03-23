from apps.buyer.apis.v110.remove_favourite.validator import \
    RemoveFavouriteValidator
from apps.buyer.models.v100.favourite import Favourite
from apps.buyer.repositories.v100.buyer_repo import BuyerRepository
from common.base_resource import BasePostResource


class RemoveFavourite(BasePostResource):
    version = 110
    end_point = 'remove_favourite'
    request_validator = RemoveFavouriteValidator()

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

    def verify_favourite(self):
        """
        Verifies that either favourite exists against user or not
        """
        is_favourite_exists = Favourite.check_favourite_existance(self.user_id, self.menu_item_id)
        if not is_favourite_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': BuyerRepository.FAVOURITE_NOT_EXISTS_MESSAGE
            }

    def remove_favourite(self):
        """
        Removes favourite menu item into db
        """
        Favourite.remove_favourite_menu_item(self.user_id, self.menu_item_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_favourite_removed': True
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_favourite()
        if self.is_send_response:
            return
        self.remove_favourite()
        self.prepare_response()
