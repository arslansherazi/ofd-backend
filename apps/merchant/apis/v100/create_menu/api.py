from apps.merchant.apis.v100.create_menu.validator import CreateMenuValidator
from apps.merchant.models.v100.menu import Menu
from apps.merchant.models.v100.merchant import Merchant
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class CreateMenu(BasePostResource):
    version = 100
    end_point = 'create_menu'
    request_validator = CreateMenuValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.name = self.request_args.get('name')
        self.image = self.request_args.get('image')
        self.is_active = self.request_args.get('is_active')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.image_url = None

    def verify_duplicate_menu(self):
        """
        Checks either menu already exists or not
        """
        menu_exists = Menu.check_duplicate_menu(self.merchant_id, self.name)
        if menu_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ALREADY_EXISTS.format(self.name)
            }

    def verify_menus_limit(self):
        """
        Checks either menus limit is exceeded or not
        """
        menus_count = Menu.get_menus_count(self.merchant_id)
        menus_limit = Merchant.get_menus_limit(self.merchant_id)
        if menus_count == menus_limit:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_LIMIT_EXCEEDS_MESSAGE.format(self.name)
            }

    def process_image(self):
        """
        process image
        """
        if self.image:
            self.image_url = MerchantRepository.process_menu_image(self.image, self.merchant_id)

    def create_menu(self):
        """
        Adds new menu into db
        """
        Menu.add_new_menu(self.merchant_id, self.name, self.image_url, self.is_active)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.MENU_CREATED_SUCCESSFULLY_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_menus_limit()
        if self.is_send_response:
            return
        self.verify_duplicate_menu()
        if self.is_send_response:
            return
        self.process_image()
        self.create_menu()
        self.prepare_response()
