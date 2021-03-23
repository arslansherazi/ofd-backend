import uuid

from apps.merchant.apis.v100.create_menu_item.validator import \
    CreateMenuItemValidator
from apps.merchant.models.v100.ingredient import Ingredient
from apps.merchant.models.v100.menu_item import MenuItem
from apps.merchant.models.v100.merchant import Merchant
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import AWS_S3_BASE_URL, PNG_IMAGE_EXTENSION


class CreateMenuItem(BasePostResource):
    version = 100
    end_point = 'create_menu_item'
    request_validator = CreateMenuItemValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.name = self.request_args.get('name')
        self.price = self.request_args.get('price')
        self.unit = self.request_args.get('unit')
        self.quantity = self.request_args.get('quantity')
        self.image = self.request_args.get('image')
        self.ingredients = self.request_args.get('ingredients')
        self.menu_id = self.request_args.get('menu_id')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.image_url = ''
        self.image_small_name = ''
        self.merchant_id = self.current_user_info.get('merchant_id')

    def verify_duplicate_menu_item(self):
        """
        Checks either menu item already exists or not
        """
        menu_item_exists = MenuItem.check_duplicate_menu_item(self.merchant_id, self.name)
        if menu_item_exists:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ITEM_ALREADY_EXISTS.format(self.name)
            }

    def verify_items_limit(self):
        """
        Checks either items limit exceeds or not
        """
        items_count = MenuItem.get_items_count(self.merchant_id)
        maximum_items_counts = Merchant.get_items_limit(self.merchant_id)
        if not items_count < maximum_items_counts:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ITEMS_LIMIT_ERROR_MESSAGE.format(maximum_items_counts)
            }

    def process_menu_item_image(self):
        """
        Process menu item image. Verifies the size of image and converts image to required size and also makes small
        image
        """
        image = CommonHelpers.process_image(image=self.image, is_menu_item_image=True)
        image_path = 'merchants/{merchant_id}/menus/{menu_id}'.format(
            merchant_id=self.merchant_id, menu_id=self.menu_id
        )
        image_name = '{image_id}.{image_extension}'.format(
            image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
        )
        self.image_url = '{base_url}/{image_path}/{image_name}'.format(
            base_url=AWS_S3_BASE_URL, image_path=image_path, image_name=image_name
        )
        CommonHelpers.put_s3_object(image, image_name, image_path)

    def save_menu_item_into_db(self):
        """
        Saves dish into db
        """
        menu_item_id = MenuItem.save_menu_item(
            self.merchant_id, self.menu_id, self.name, self.unit, self.quantity, self.price, self.image_url
        )
        Ingredient.save_menu_item_ingredients(menu_item_id, self.ingredients)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.MENU_ITEM_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_duplicate_menu_item()
        self.verify_items_limit()
        if self.is_send_response:
            return
        self.process_menu_item_image()
        self.save_menu_item_into_db()
        self.prepare_response()
