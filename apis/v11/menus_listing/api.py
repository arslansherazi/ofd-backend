from common.base_resource import BaseGetResource
from models.menu import Menu
from repositories.v11.merchant_repo import MerchantRepository


class MenusListing(BaseGetResource):
    version = 11
    end_point = 'menus_listing'

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.menus = []
        self.merchant_id = self.current_user_info.get('merchant_id')

    def initialize_models(self):
        """
        Initializes models
        """
        self.menu_model = Menu()

    def initialize_repositories(self):
        """
        Initializes repositories
        """
        self.merchant_repo = MerchantRepository()

    def get_menus(self):
        """
        Gets menus
        """
        self.menus = self.menu_model.get_menus(self.merchant_id)
        if not self.menus:
            self.status_code = 422
            self.is_send_response = True
            self.response = {
                'message': self.merchant_repo.NO_MENU_EXISTS_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'menus': self.menus
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.initialize_models()
        self.initialize_repositories()
        self.get_menus()
        if self.is_send_response:
            return
        self.prepare_response()
