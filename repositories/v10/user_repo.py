import uuid

from common.common_helpers import CommonHelpers
from common.constants import (IMAGES_BASE_URL, MERCHANT_USER_TYPE,
                              PNG_IMAGE_EXTENSION)


class UserRepository(object):
    USERNAME_ALREADY_EXIST = 'username already exists'
    USER_LOGGEDIN_ERROR_MESSAGE = 'Password is incorrect'
    EMAIL_VERIFICATION_MESSAGE = 'Email is not verified yet'
    USER_NOT_EXISTS_IN_SYSTEM_MESSAGE = 'user does not exist in system'
    EMAIL_EXISTS_IN_SYSTEM_MESSAGE = 'email already registered with us. Please register with some other email'
    EMAIL_ALREADY_REGISTERED_MESSAGE = '{} already registered with us. Please use other email address'
    PASSWORD_UPDATE_SUCCESS_MESSAGE = 'Password is updated successfully'
    INVALID_PASSWORD_MESSAGE = 'Old password is invalid'
    EXPIRED_VERIFICATION_CODE_MESSAGE = 'Verification code is expired'
    INVALID_VERIFICATION_MESSAGE = 'Verification code is invalid'
    PROFILE_UPDATE_MESSAGE = 'Profile is updated successfully'
    EMAIL_VERIFICATION_CODE_MESSAGE = 'An email is sent to your email address. Please verify your email'
    NEW_EMAIL_VERIFICATION_MESSAGE = 'An email is sent to your email address. Please verify your email. Email will only change after verification'  # noqa: 501
    EMAIL_NOT_EXISTS_MESSAGE = '{} is not registered with us'

    @staticmethod
    def upload_profile_image(user_type, image=None, buyer_id=None, merchant_id=None):
        """
        Uploads profile image. It also generates profile image url for database

        :param int user_type: user type
        :param Image image: image
        :param int buyer_id: buyer id
        :param int merchant_id: merchant id
        """
        image = CommonHelpers.process_image(image=image, is_profile_image=True)
        image_name = '{image_id}.{image_extension}'.format(
            image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
        )
        if user_type == MERCHANT_USER_TYPE:
            image_path = 'merchants/{merchant_id}/profile'.format(merchant_id=merchant_id)
            CommonHelpers.upload_image(image, image_name, image_path)
            profile_image_url = '{base_url}/{image_path}/{image_name}'.format(
                base_url=IMAGES_BASE_URL, image_path=image_path, image_name=image_name
            )
        else:
            image_path = 'buyers/{buyer_id}/profile'.format(buyer_id=buyer_id)
            CommonHelpers.upload_image(image, image_name, image_path)
            profile_image_url = '{base_url}/{image_path}/{image_name}'.format(
                base_url=IMAGES_BASE_URL, image_path=image_path, image_name=image_name
            )
        return profile_image_url
