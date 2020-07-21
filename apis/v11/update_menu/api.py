from apis.v11.update_menu.validator import UpdateMenuValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from models.menu import Menu
from repositories.v11.merchant_repo import MerchantRepository


class UpdateMenu(BasePostResource):
    version = 11
    end_point = 'update_menu'
    request_validator = UpdateMenuValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_id = self.request_args.get('menu_id')
        self.name = self.request_args.get('name')
        self.image = self.request_args.get('image')
        self.is_activate = bool(int(self.request_args.get('is_activate')))
        self.is_deactivate = bool(int(self.request_args.get('is_deactivate')))

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.image_url = None

    def process_image(self):
        """
        Deletes old menu image
        """
        if self.image:
            old_menu_image_url = Menu.get_menu_image_url(self.menu_id)
            if old_menu_image_url:
                old_profile_image_name = old_menu_image_url.split('/')[-1]
                delete_file_path = 'uploads/merchants/{merchant_id}/menus'
                delete_file_path = delete_file_path.format(
                    merchant_id=self.merchant_id, image_name=old_profile_image_name
                )
                CommonHelpers.remove_file(delete_file_path, old_profile_image_name)
            self.image_url = MerchantRepository.process_menu_image(self.image, self.merchant_id)

    def update_menu(self):
        """
        Updates menu details. It also verifies that either menu exists or not against the merchant
        """
        menu = Menu.update_menu(
            self.menu_id, self.merchant_id, self.name, self.image_url, self.is_activate, self.is_deactivate
        )
        if not menu:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_NOT_EXIST_MESSAGE
            }

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.MENU_UPDATE_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.process_image()
        self.update_menu()
        if self.is_send_response:
            return
        self.prepare_response()
