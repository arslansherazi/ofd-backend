import uuid
from datetime import datetime

from common.common_helpers import CommonHelpers
from common.constants import AWS_S3_BASE_URL, PNG_IMAGE_EXTENSION
from models.merchant import Merchant


class MerchantRepository(object):
    ITEMS_LIMIT_ERROR_MESSAGE = 'Sorry, You cannot offer more than {} dishes'
    MENU_ITEM_SUCCESS_MESSAGE = 'Your menu item is offered successfully'
    NO_MENU_EXISTS_MESSAGE = 'You did not create any menu yet'
    NO_MENU_ITEM_EXISTS_MESSAGE = 'You did not create any item in this menu'
    MENU_ITEM_ALREADY_EXISTS = '{} is already offered'
    MENU_ALREADY_EXISTS = '{} menu already exists'
    MENU_LIMIT_EXCEEDS_MESSAGE = 'Your limit of menus exceeds'
    MENU_CREATED_SUCCESSFULLY_MESSAGE = 'menu is created successfully'
    NO_ORDERS_MESSAGE = 'No order exists'
    ORDER_NOT_EXISTS_MESSAGE = 'Order does not exist'
    STATUS_CHANGED_MESSAGE = 'status is updated successfully'
    PlACED_ORDER_STATUS = 'Placed'
    ACCEPTED_ORDER_STATUS = 'Accepted'
    REJECTED_ORDER_STATUS = 'Rejected'
    CANCELLED_ORDER_STATUS = 'Cancelled'
    ON_ROUTE_ORDER_STATUS = 'On Route'
    COMPLETED_ORDER_STATUS = 'Completed'
    ORDER_STATUS_CHANGE_ERROR_MESSAGE = 'Order is {}. You cannot change status of this order'
    MENU_NOT_EXIST_MESSAGE = 'Menu does not exist'
    MENU_UPDATE_SUCCESS_MESSAGE = 'Menu is updated successfully'
    MENU_DELETED_SUCCESSFULLY_MESSAGE = 'Menu is deleted successfully'
    MENU_CONTAINS_ORDERS_MESSAGE = 'Some of the items in the menu are participating in running orders. Please complete these orders first to delete this menu'  # noqa: 501
    ORDER_FAILED_MESSAGE = 'Order cannot be {}'
    ORDER_SUCCESS_MESSAGE = 'Order is {} successfully'
    ORDER_SAME_STATUS_MESSAGE = 'Order is already {}'
    MENU_ITEM_NOT_EXIST_MESSAGE = 'Menu item does not exist'
    MENU_ITEM_ORDERS_MESSAGE = 'Some running orders contain this item. Please complete these orders to update this item'  # noqa: 501
    MENU_ITEM_UPDATE_SUCCESS_MESSAGE = 'Menu item is updated successfully'
    MENU_ITEM_DELETION_SUCCESS_MESSAGE = 'Menu item is deleted successfully'
    USER_DELETION_ORDERS_MESSAGE = 'You have some running orders. Please complete these orders to delete your account'
    UPDATE_TIMINGS_SUCCESS_MESSAGE = 'Your Timings are successfully updated'
    ALL_WEEK_MERCHANT_AVAILABILITY = 'All Week'
    MERCHANT_NOT_EXISTS_MESSAGE = '{} is no longer available'
    INVALID_ADDRESS_MESSAGE = 'Address is not correct'
    INVALID_LOCATION_ADDRESS_MESSAGE = 'Sorry\nThis address does not lie within your location'
    NOTIFICATION_BODY = 'You order from {merchant_name} is {status}'

    @staticmethod
    def verify_merchant_availability(merchant_id):
        """
        verifies that either merchant is online or not
        """
        is_merchant_online = True
        merchant_availability = Merchant.get_merchant_availability(merchant_id)
        is_open_all_day = merchant_availability.get('is_open_all_day')
        is_open_all_week = merchant_availability.get('is_open_all_week')
        opening_time = merchant_availability.get('opening_time')
        closing_time = merchant_availability.get('closing_time')
        opening_days = merchant_availability.get('opening_days')
        if opening_days:
            opening_days = opening_days.split('')
        else:
            opening_days = []
        if not is_open_all_day:
            current_time = datetime.now().time()
            if not opening_time <= current_time <= closing_time:
                is_merchant_online = False
        if not is_open_all_week and is_merchant_online:
            current_day = datetime.today().strftime('%A')
            if current_day not in opening_days:
                is_merchant_online = False
        if is_merchant_online:
            return {'is_merchant_online': True}
        if is_open_all_week:
            merchant_opening_days = MerchantRepository.ALL_WEEK_MERCHANT_AVAILABILITY
        else:
            merchant_opening_days = opening_days[0]
            for opening_day in opening_days[1:]:
                merchant_opening_days += ' - {}'.format(opening_day)
        message = '{merchant_name} is currently offline\nOpening Hours: {opening_time} - {closing_time}\nOpening Days: {opening_days}'.format(  # noqa: 501
            merchant_name=merchant_availability.get('name'),
            opening_time=merchant_availability.get('opening_time'),
            closing_time=merchant_availability.get('closing_time'),
            opening_days=merchant_opening_days
        )
        return {
            'is_merchant_online': False,
            'message': message
        }

    @staticmethod
    def process_menu_image(image, merchant_id):
        """
        Process menu image

        :param Image image: menu image file
        :param int merchant_id: merchant id

        :rtype str
        :returns image url
        """
        image = CommonHelpers.process_image(image=image, is_menu_image=True)
        image_path = 'merchants/{merchant_id}/menus'.format(merchant_id=merchant_id)
        image_name = '{image_id}.{image_extension}'.format(
            image_id=str(uuid.uuid4()), image_extension=PNG_IMAGE_EXTENSION
        )
        CommonHelpers.put_s3_object(image, image_name, image_path)
        image_url = '{base_url}/{image_path}/{image_name}'.format(
            base_url=AWS_S3_BASE_URL, image_path=image_path, image_name=image_name
        )
        return image_url
