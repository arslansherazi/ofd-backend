import uuid

from apps.buyer.models.v100.order import Order
from apps.buyer.models.v100.order_details import OrderDetails
from apps.merchant.apis.v100.update_menu_item.validator import \
    UpdateMenuItemValidator
from apps.merchant.models.v100.ingredient import Ingredient
from apps.merchant.models.v100.menu_item import MenuItem
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import AWS_S3_BASE_URL, PNG_IMAGE_EXTENSION


class UpdateMenuItem(BasePostResource):
    version = 100
    end_point = 'update_menu_item'
    request_validator = UpdateMenuItemValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.menu_item_id = self.request_args.get('menu_item_id')
        self.name = self.request_args.get('name')
        self.unit = self.request_args.get('unit')
        self.price = self.request_args.get('price')
        self.quantity = self.request_args.get('quantity')
        self.image = self.request_args.get('image')
        self.discount = self.request_args.get('discount')
        self.is_activated = self.request_args.get('is_activated')
        self.is_deactivated = self.request_args.get('is_deactivated')
        self.ingredients = self.request_args.get('ingredients')

    def initialize_class_attributes(self):
        """
        initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.image_url = ''

    def verify_menu_item(self):
        """
        Verifies that either menu item exists or not against the merchant
        """
        self.menu_item = MenuItem.get_menu_item(self.menu_item_id, self.merchant_id)
        if not self.menu_item:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ITEM_NOT_EXIST_MESSAGE
            }

    def check_menu_item_orders(self):
        """
        Checks menu item orders. If menu item is participating in any running order then we cannot update it
        """
        menu_item_orders = OrderDetails.verify_menu_item_orders(self.menu_item_id)
        if menu_item_orders:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.MENU_ITEM_ORDERS_MESSAGE
            }

    def process_image(self):
        """
        Process image. It also deleted the old image of menu item
        """
        if self.image:
            image = CommonHelpers.process_image(self.image, is_menu_item_image=True)
            image_path = 'merchants/{merchant_id}/menus/{menu_id}'.format(
                merchant_id=self.merchant_id, menu_id=self.menu_item.get('menu_id')
            )
            delete_image_path = 'uploads/merchants/{merchant_id}/menus/{menu_id}'.format(
                merchant_id=self.merchant_id, menu_id=self.menu_item.get('menu_id')
            )
            old_image_name = self.menu_item.get('image_url').split('/')[-1]
            image_name = '{image_id}.{image_extension}'.format(
                image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
            )
            self.image_url = '{base_url}/{image_path}/{image_name}'.format(
                base_url=AWS_S3_BASE_URL, image_path=image_path, image_name=image_name
            )
            CommonHelpers.delete_aws_s3_file(delete_image_path, old_image_name)
            CommonHelpers.put_s3_object(image, image_name, image_path)

    def update_menu_item(self):
        """
        Updates menu item. It also updates orders history to notify buyer that item details has been changed while
        reorder this item
        """
        MenuItem.update_menu_item(
            self.menu_item_id, self.name, self.unit, self.price, self.quantity, self.image_url, self.discount,
            self.is_activated, self.is_deactivated
        )
        menu_item_orders_ids = OrderDetails.get_menu_item_orders_ids(self.menu_item_id)
        if menu_item_orders_ids:
            Order.update_orders_price_changed_flag(menu_item_orders_ids, flag=True)

    def update_menu_item_ingredients(self):
        """
        Updates menu item ingredients
        """
        if self.ingredients:
            deleted_ingredients_ids = []
            updated_ingredients = []
            added_ingredients = []
            for ingredient in self.ingredients:
                if ingredient.get('is_removed', False):
                    deleted_ingredients_ids.append(ingredient.get('id'))
                else:
                    ingredient_details = {
                        'name': ingredient.get('name'),
                        'quantity': ingredient.get('quantity'),
                        'unit': ingredient.get('quantity'),
                    }
                    if ingredient.get('is_updated'):
                        ingredient_details.update(id=ingredient.get('id'))
                        updated_ingredients.append(ingredient_details)
                    else:
                        added_ingredients.append(ingredient_details)
            if deleted_ingredients_ids:
                Ingredient.delete_ingredients(deleted_ingredients_ids)
            if updated_ingredients:
                Ingredient.update_ingredients(updated_ingredients)
            if added_ingredients:
                Ingredient.save_menu_item_ingredients(self.menu_item_id, added_ingredients)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.MENU_ITEM_UPDATE_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.verify_menu_item()
        if self.is_send_response:
            return
        self.check_menu_item_orders()
        if self.is_send_response:
            return
        self.process_image()
        self.update_menu_item()
        self.update_menu_item_ingredients()
        self.prepare_response()
