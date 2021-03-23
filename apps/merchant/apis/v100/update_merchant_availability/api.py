from apps.merchant.apis.v100.update_merchant_availability.validator import \
    UpdateMerchantAvailabilityValidator
from apps.merchant.models.v100.merchant import Merchant
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class UpdateMerchantAvailability(BasePostResource):
    version = 100
    end_point = 'update_merchant_availability'
    request_validator = UpdateMerchantAvailabilityValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.opening_time = self.request_args.get('opening_time')
        self.closing_time = self.request_args.get('closing_time')
        self.opening_days = self.request_args.get('opening_days')
        self.is_open_all_day = self.request_args.get('is_open_all_day')
        self.is_open_all_week = self.request_args.get('is_open_all_week')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')

    def update_merchant_availability(self):
        """
        Updates merchant availability
        """
        Merchant.update_merchant_availability(
            self.merchant_id, self.opening_time, self.closing_time, self.opening_days, self.is_open_all_day,
            self.is_open_all_week
        )

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'message': MerchantRepository.UPDATE_TIMINGS_SUCCESS_MESSAGE
        }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.update_merchant_availability()
        self.prepare_response()
