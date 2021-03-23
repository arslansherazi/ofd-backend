from apps.buyer.models.v100.notifications_token import NotificationsToken
from apps.buyer.models.v100.order import Order
from apps.buyer.models.v100.order_details import OrderDetails
from apps.merchant.apis.v100.update_order_status.validation import \
    UpdateOrderStatusValidator
from apps.merchant.models.v100.driver import Driver
from apps.merchant.models.v100.merchant import Merchant
from apps.merchant.models.v100.report import Report
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource
from common.common_helpers import CommonHelpers


class UpdateOrderStatus(BasePostResource):
    version = 100
    end_point = 'update_order_status'
    request_validator = UpdateOrderStatusValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.order_id = self.request_args.get('order_id')
        self.buyer_id = self.request_args.get('buyer_id')
        self.status = self.request_args.get('status')
        if self.status == MerchantRepository.ON_ROUTE_ORDER_STATUS:
            self.first_name = self.request_args.get('driver_info').get('first_name')
            self.last_name = self.request_args.get('driver_info').get('last_name')
            self.vehicle_model = self.request_args.get('driver_info').get('vehicle_model')
            self.vehicle_number = self.request_args.get('driver_info').get('vehicle_number')
            self.contact_no = self.request_args.get('driver_info').get('contact_no')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')

    def update_order_status(self):
        """
        Updates order status
        """
        order_status = Order.get_order_status(self.order_id, self.merchant_id, self.buyer_id)
        if order_status:
            if (
                    self.status in [MerchantRepository.ACCEPTED_ORDER_STATUS, MerchantRepository.REJECTED_ORDER_STATUS]
                    and order_status != MerchantRepository.PlACED_ORDER_STATUS
            ):
                self.is_send_response = True
                self.status_code = 422
                if self.status == order_status:
                    self.response = {
                        'message': MerchantRepository.ORDER_SAME_STATUS_MESSAGE.format(self.status.lower())
                    }
                else:
                    self.response = {
                        'message': MerchantRepository.ORDER_FAILED_MESSAGE.format(self.status.lower())
                    }
            elif order_status == self.status:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': MerchantRepository.ORDER_SAME_STATUS_MESSAGE.format(self.status.lower())
                }
            elif order_status in [MerchantRepository.REJECTED_ORDER_STATUS, MerchantRepository.COMPLETED_ORDER_STATUS]:
                self.is_send_response = True
                self.status_code = 422
                self.response = {
                    'message': MerchantRepository.ORDER_STATUS_CHANGE_ERROR_MESSAGE.format(order_status.lower())
                }
            else:
                Order.update_order_status(self.order_id, self.status)
                notifications_token = NotificationsToken.get_notifications_token(self.buyer_id)
                merchant_profile = Merchant.get_profile(self.merchant_id)
                notification_body = MerchantRepository.NOTIFICATION_BODY.format(
                    merchant_name=merchant_profile.get('name'), status=self.status
                )
                notification_data = OrderDetails.get_buyer_orders(order_id=self.order_id)
                CommonHelpers.send_push_notification(notifications_token, notification_body, notification_data)
        else:
            self.is_send_response = True
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.ORDER_NOT_EXISTS_MESSAGE
            }

    def update_driver_info(self):
        """
        Updates driver info
        """
        if self.status == MerchantRepository.ON_ROUTE_ORDER_STATUS:
            Driver.add_driver(
                self.order_id, self.first_name, self.last_name, self.vehicle_model, self.vehicle_number, self.contact_no
            )

    def update_merchant_orders_report(self):
        """
        Updates merchant orders report
        """
        if self.status == MerchantRepository.COMPLETED_ORDER_STATUS:
            order_price = Order.get_order_price(self.order_id)
            Report.update_report(self.merchant_id, order_price)

    def prepare_response(self):
        """
        Prepares response
        """
        if self.status in [MerchantRepository.ACCEPTED_ORDER_STATUS, MerchantRepository.REJECTED_ORDER_STATUS]:
            self.response = {
                'message': MerchantRepository.ORDER_SUCCESS_MESSAGE.format(self.status.lower())
            }
        else:
            self.response = {
                'data': {
                    'is_status_changed': True,
                    'message': MerchantRepository.STATUS_CHANGED_MESSAGE
                }
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.update_order_status()
        if self.is_send_response:
            return
        self.update_driver_info()
        self.update_merchant_orders_report()
        self.prepare_response()
