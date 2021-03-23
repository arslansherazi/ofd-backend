from apps.buyer.models.v100.order_details import OrderDetails
from apps.merchant.apis.v100.merchant_orders_listing.validation import \
    MerchantOrdersListingValidator
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.base_resource import BasePostResource


class MerchantOrdersListing(BasePostResource):
    version = 100
    end_point = 'merchant_orders_listing'
    request_validator = MerchantOrdersListingValidator()

    def populate_request_arguments(self):
        """
        Populates request arguments
        """
        self.offset = self.request_args.get('offset')
        self.limit = self.request_args.get('limit')
        self.filters = self.request_args.get('filters')

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.orders_exist = False

    def get_orders(self):
        """
        Gets orders
        """
        self.orders = OrderDetails.get_merchant_orders(self.merchant_id, **self.filters)
        if self.orders:
            self.orders_exist = True

    def prepare_response(self):
        """
        Prepares response
        """
        if self.orders_exist:
            self.response = {
                'data': {
                    'orders': self.orders[self.offset:self.offset + self.limit]
                }
            }
        else:
            self.status_code = 422
            self.response = {
                'message': MerchantRepository.NO_ORDERS_MESSAGE
            }

    def process_request(self):
        """
        Process request
        """
        self.populate_request_arguments()
        self.initialize_class_attributes()
        self.get_orders()
        self.prepare_response()
