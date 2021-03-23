import uuid

from apps.buyer.models.v100.buyer import Buyer
from apps.merchant.models.v100.merchant import Merchant
from apps.user.apis.v100.signup.validator import SignupValidator
from apps.user.models import User
from apps.user.repositories.v100.user_repo import UserRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import (AWS_S3_BASE_URL, MERCHANT_USER_TYPE,
                              PNG_IMAGE_EXTENSION)


class Signup(BasePostResource):
    version = 100
    end_point = 'signup'
    request_validator = SignupValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.username = self.request_args.get('username')
        self.email = self.request_args.get('email')
        self.password = self.request_args.get('password')
        self.user_type = int(self.request_args.get('user_type'))
        self.image = self.request_args.get('image')
        if self.user_type == MERCHANT_USER_TYPE:
            self.name = self.request_args.get('name')
            self.title = self.request_args.get('title')
            self.contact_no = self.request_args.get('contact_no')
            self.address = self.request_args.get('address')
            self.latitude = self.request_args.get('latitude')
            self.longitude = self.request_args.get('longitude')
            self.location_id = self.request_args.get('location_id')
            self.menus_limit = self.request_args.get('menus_limit')
            self.items_limit = self.request_args.get('items_limit')
            self.is_takeaway_enabled = self.request_args.get('is_takeaway_enabled')
            self.is_delivery_enabled = self.request_args.get('is_delivery_enabled')
            self.opening_time = self.request_args.get('opening_time')
            self.closing_time = self.request_args.get('closing_time')
            self.opening_days = self.request_args.get('opening_days')
            self.is_open_all_day = self.request_args.get('is_open_all_day')
            self.is_open_all_week = self.request_args.get('is_open_all_week')
        else:
            self.first_name = self.request_args.get('first_name')
            self.last_name = self.request_args.get('last_name')

    def initialize_class_attributes(self):
        self.profile_image_url = ''

    def check_username_availability(self):
        """
        Checks that either username is available or not
        """
        self.is_username_available = User.check_username_availability(self.username, self.user_type)
        if not self.is_username_available:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': UserRepository.USERNAME_ALREADY_EXIST,
                'is_signed_up': False
            }

    def check_email_availability(self):
        """
        Checks that either email is available or not
        """
        self.is_email_exists_in_system = User.check_email_availability(self.email, self.user_type)
        if self.is_email_exists_in_system:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': UserRepository.EMAIL_EXISTS_IN_SYSTEM_MESSAGE,
                'is_signed_up': False
            }

    def insert_user_into_db(self):
        """
        Adds user into the system
        """
        self.user_id = User.insert_user_into_db(
            self.username, self.email, self.password, self.profile_image_url, self.user_type
        )
        if self.user_type == MERCHANT_USER_TYPE:
            self.merchant_id = Merchant.insert_merchant_into_db(
                self.user_id, self.name, self.title, self.contact_no, self.address, self.latitude, self.longitude,
                self.location_id, self.menus_limit, self.items_limit, self.is_takeaway_enabled,
                self.is_delivery_enabled, self.opening_time, self.closing_time, self.opening_days, self.is_open_all_day,
                self.is_open_all_week
            )
        else:
            self.buyer_id = Buyer.insert_buyer_into_db(
                self.user_id, self.first_name, self.last_name
            )

    def upload_profile_image(self):
        """
        Uploads profile image. It also generates profile image url for database
        """
        if self.image:
            image = CommonHelpers.process_image(image=self.image, is_profile_image=True)
            image_name = '{image_id}.{image_extension}'.format(
                image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
            )
            if self.user_type == MERCHANT_USER_TYPE:
                image_path = 'merchants/{merchant_id}/profile'.format(merchant_id=self.merchant_id)
                CommonHelpers.put_s3_object(image, image_name, image_path)
                self.profile_image_url = '{base_url}/{image_path}/{image_name}'.format(
                    base_url=AWS_S3_BASE_URL, image_path=image_path, image_name=image_name
                )
            else:
                image_path = 'buyers/{buyer_id}/profile'.format(buyer_id=self.buyer_id)
                CommonHelpers.put_s3_object(image, image_name, image_path)
                self.profile_image_url = '{base_url}/{image_path}/{image_name}'.format(
                    base_url=AWS_S3_BASE_URL, image_path=image_path, image_name=image_name
                )

    def insert_profile_image_url_into_db(self):
        """
        Inserts profile image url into db
        """
        User.update_profile_image_url(self.user_id, self.profile_image_url)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'is_signed_up': True
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.check_username_availability()
        if self.is_send_response:
            return
        self.check_email_availability()
        if self.is_send_response:
            return
        self.insert_user_into_db()
        self.upload_profile_image()
        self.insert_profile_image_url_into_db()
        self.prepare_response()
