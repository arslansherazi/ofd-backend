from rest_framework_simplejwt import views as jwt_views

from apps.buyer.apis.v100.add_new_address.api import AddNewAddress
from apps.buyer.apis.v100.add_notifications_token.api import AddNotificationsToken
from apps.buyer.apis.v100.buyer_orders_listing.api import BuyerOrdersListing
from apps.buyer.apis.v100.cancel_order.api import CancelOrder
from apps.buyer.apis.v100.delete_address.api import DeleteAddress
from apps.buyer.apis.v100.feedback.api import FeedbackApi
from apps.buyer.apis.v100.get_addresses.api import GetAddresses
from apps.buyer.apis.v100.get_feedbacks.api import GetFeedbacks
from apps.buyer.apis.v100.get_location_id.api import GetLocationId
from apps.buyer.apis.v100.home.api import Home
from apps.buyer.apis.v100.item_details.api import MenuItemDetails
from apps.buyer.apis.v100.items_listing.api import ItemsListing
from apps.buyer.apis.v100.location.api import VerifyLocation
from apps.buyer.apis.v100.make_tiny_url.api import MakeTinyUrl
from apps.buyer.apis.v100.merchants.api import Merchants
from apps.buyer.apis.v100.order_status.api import OrderStatus
from apps.buyer.apis.v100.place_order.api import PlaceOrder
from apps.buyer.apis.v100.reorder.api import Reorder
from apps.buyer.apis.v100.update_address.api import UpdateAddress
from apps.buyer.apis.v100.update_order.api import UpdateOrder
from apps.merchant.apis.v100.create_menu.api import CreateMenu
from apps.merchant.apis.v100.create_menu_item.api import CreateMenuItem
from apps.merchant.apis.v100.delete_menu.api import DeleteMenu
from apps.merchant.apis.v100.delete_menu_item.api import DeleteMenuItem
from apps.merchant.apis.v100.menu_items_listing.api import MenuItemsListing
from apps.merchant.apis.v100.menus_listing.api import MenusListing
from apps.merchant.apis.v100.merchant_orders_listing.api import MerchantOrdersListing
from apps.merchant.apis.v100.order_details.api import OrderDetailsApi
from apps.merchant.apis.v100.update_menu.api import UpdateMenu
from apps.merchant.apis.v100.update_menu_item.api import UpdateMenuItem
from apps.merchant.apis.v100.update_merchant_availability.api import UpdateMerchantAvailability
from apps.merchant.apis.v100.update_order_status.api import UpdateOrderStatus
from apps.merchant.apis.v110.report.api import ReportApi
from apps.user.apis.v100.change_password.api import ChangePassword
from apps.user.apis.v100.delete_user.api import DeleteUser
from apps.user.apis.v100.get_profile.api import GetProfile
from apps.user.apis.v100.login.api import Login
from apps.user.apis.v100.send_email.api import SendEmail
from apps.user.apis.v100.signup.api import Signup
from apps.user.apis.v100.validate_email.api import ValidateEmail
from apps.user.apis.v100.verify_email.api import VerifyEmail
from routing.base_routing import BaseRouting


class RoutingV100(BaseRouting):
    api_version = '100'

    def set_routing_collection(self):
        self.routing_collection = {
            'login': Login,
            'signup': Signup,
            'validate_email': ValidateEmail,
            'send_email': SendEmail,
            'change_password': ChangePassword,
            'verify_email': VerifyEmail,
            'delete_user': DeleteUser,
            'get_profile': GetProfile,
            'create_menu': CreateMenu,
            'create_menu_item': CreateMenuItem,
            'menus_listing': MenusListing,
            'menu_items_listing': MenuItemsListing,
            'merchant_orders_listing': MerchantOrdersListing,
            'order_details': OrderDetailsApi,
            'update_order_status': UpdateOrderStatus,
            'update_menu': UpdateMenu,
            'delete_menu': DeleteMenu,
            'update_menu_item': UpdateMenuItem,
            'delete_menu_item': DeleteMenuItem,
            'update_merchant_availability': UpdateMerchantAvailability,
            'api_token': jwt_views.TokenObtainPairView,
            'place_order': PlaceOrder,
            'buyer_orders_listing': BuyerOrdersListing,
            'feedback': FeedbackApi,
            'order_status': OrderStatus,
            'cancel_order': CancelOrder,
            'update_order': UpdateOrder,
            'reorder': Reorder,
            'home': Home,
            'items_listing': ItemsListing,
            'report': ReportApi,
            'verify_location': VerifyLocation,
            'merchants': Merchants,
            'item_details': MenuItemDetails,
            'get_location_id': GetLocationId,
            'add_new_address': AddNewAddress,
            'get_addresses': GetAddresses,
            'update_address': UpdateAddress,
            'delete_address': DeleteAddress,
            'make_tiny_url': MakeTinyUrl,
            'get_feedbacks': GetFeedbacks,
            'add_notifications_token': AddNotificationsToken
        }
