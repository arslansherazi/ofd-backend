from apis.models import User
from apis.v10.update_profile.validator import UpdateProfileValidator
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers
from common.constants import (BUYER_USER_TYPE, BUYERS, MERCHANT_USER_TYPE,
                              MERCHANTS)
from models.buyer import Buyer
from models.merchant import Merchant
from repositories.v10.user_repo import UserRepository
from repositories.v11.user_repo import UserRepositoryV11


class UpdateProfile(BasePostResource):
    version = 10
    end_point = 'update_profile'
    request_validator = UpdateProfileValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.user_type = int(self.request_args.get('user_type'))
        self.username = self.request_args.get('username')
        self.profile_image = self.request_args.get('profile_image')
        if self.user_type == MERCHANT_USER_TYPE:
            self.name = self.request_args.get('name')
            self.title = self.request_args.get('title')
            self.contact_no = self.request_args.get('contact_no')
            self.address = self.request_args.get('address')
            self.latitude = self.request_args.get('latitude')
            self.longitude = self.request_args.get('longitude')
            self.is_delivery_enabled = bool(self.request_args.get('is_delivery_enabled'))
            self.is_takeaway_enabled = bool(self.request_args.get('is_takeaway_enabled'))
        else:
            self.first_name = self.request_args.get('first_name')
            self.last_name = self.request_args.get('last_name')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.user_id = self.current_user_info.get('user_id')
        self.profile_image_url = None
        if self.user_type == BUYER_USER_TYPE:
            self.buyer_id = self.current_user_info.get('buyer_id')
        else:
            self.merchant_id = self.current_user_info.get('merchant_id')

    def process_profile_image(self):
        """
        Process profile image

        1. Deletes old profile image
        2. Uploads new profile image
        """
        old_profile_image_url = User.get_profile_image_url(self.user_id)
        if old_profile_image_url:
            old_profile_image_name = old_profile_image_url.split('/')[-1]
            delete_file_path = 'uploads/{user}/{user_id}/profile'
            if self.user_type == BUYER_USER_TYPE:
                delete_file_path = delete_file_path.format(
                    user=BUYERS, user_id=self.buyer_id
                )
            else:
                delete_file_path = delete_file_path.format(
                    user=MERCHANTS, user_id=self.merchant_id
                )
            CommonHelpers.remove_file(delete_file_path, old_profile_image_name)
        if self.user_type == BUYER_USER_TYPE:
            self.profile_image_url = UserRepository.upload_profile_image(
                user_type=BUYER_USER_TYPE, image=self.profile_image, buyer_id=self.buyer_id
            )
        else:
            self.profile_image_url = UserRepository.upload_profile_image(
                user_type=MERCHANT_USER_TYPE, image=self.profile_image, merchant_id=self.merchant_id
            )

    def check_username_availability(self):
        if self.username:
            is_username_available = User.check_username_availability(self.username, self.user_type)
            if not is_username_available:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': UserRepositoryV11.USERNAME_ALREADY_EXIST
                }

    def update_profile(self):
        """
        Updates profile details
        """
        if self.profile_image_url or self.username:
            User.update_data(self.user_id, self.username, self.profile_image_url)
        if self.user_type == BUYER_USER_TYPE:
            if self.first_name and self.last_name:
                Buyer.update_data(self.buyer_id, self.first_name, self.last_name)
        else:
            Merchant.update_data(
                self.merchant_id, self.name, self.title, self.contact_no, self.address, self.latitude, self.longitude,
                self.is_delivery_enabled, self.is_takeaway_enabled
            )

    def prepare_response(self):
        """
        Prepares Response
        """
        self.response = {
            'data': {
                'is_profile_updated': True,
                'message': UserRepository.PROFILE_UPDATE_MESSAGE
            }
        }
        if self.profile_image_url:
            self.response['data'].update(profile_image_url=self.profile_image_url)
        if self.username:
            self.response['data'].update(message=UserRepositoryV11.USERNAME_UPDTED_SUCCESSFULLY)

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        if self.profile_image:
            self.process_profile_image()
        self.check_username_availability()
        if self.is_send_response:
            return
        self.update_profile()
        self.prepare_response()
