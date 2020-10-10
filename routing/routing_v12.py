from apis.v11.report.api import ReportApi
from apis.v12.add_favourite.api import AddFavourite
from apis.v12.add_new_address.api import AddNewAddress
from apis.v12.add_notifications_token.api import AddNotificationsToken
from apis.v12.buyer_orders_listing.api import BuyerOrdersListing
from apis.v12.cancel_order.api import CancelOrder
from apis.v12.delete_address.api import DeleteAddress
from apis.v12.favourites_listing.api import FavouritesListing
from apis.v12.feedback.api import FeedbackApi
from apis.v12.get_addresses.api import GetAddresses
from apis.v12.get_feedbacks.api import GetFeedbacks
from apis.v12.get_location_id.api import GetLocationId
from apis.v12.home.api import Home
from apis.v12.item_details.api import MenuItemDetails
from apis.v12.items_listing.api import ItemsListing
from apis.v12.location.api import VerifyLocation
from apis.v12.make_tiny_url.api import MakeTinyUrl
from apis.v12.merchants.api import Merchants
from apis.v12.order_status.api import OrderStatus
from apis.v12.place_order.api import PlaceOrder
from apis.v12.remove_favourite.api import RemoveFavourite
from apis.v12.reorder.api import Reorder
from apis.v12.update_address.api import UpdateAddress
from apis.v12.update_order.api import UpdateOrder
from routing.routing_v11 import RoutingV11


class RoutingV12(RoutingV11):
    api_version = '12'

    def set_routing_collection(self):
        super().set_routing_collection()
        self.routing_collection['place_order'] = PlaceOrder
        self.routing_collection['buyer_orders_listing'] = BuyerOrdersListing
        self.routing_collection['feedback'] = FeedbackApi
        self.routing_collection['order_status'] = OrderStatus
        self.routing_collection['cancel_order'] = CancelOrder
        self.routing_collection['update_order'] = UpdateOrder
        self.routing_collection['reorder'] = Reorder
        self.routing_collection['home'] = Home
        self.routing_collection['items_listing'] = ItemsListing
        self.routing_collection['report'] = ReportApi
        self.routing_collection['verify_location'] = VerifyLocation
        self.routing_collection['add_favourite'] = AddFavourite
        self.routing_collection['remove_favourite'] = RemoveFavourite
        self.routing_collection['favourites_listing'] = FavouritesListing
        self.routing_collection['merchants'] = Merchants
        self.routing_collection['item_details'] = MenuItemDetails
        self.routing_collection['get_location_id'] = GetLocationId
        self.routing_collection['add_new_address'] = AddNewAddress
        self.routing_collection['get_addresses'] = GetAddresses
        self.routing_collection['update_address'] = UpdateAddress
        self.routing_collection['delete_address'] = DeleteAddress
        self.routing_collection['make_tiny_url'] = MakeTinyUrl
        self.routing_collection['get_feedbacks'] = GetFeedbacks
        self.routing_collection['add_notifications_token'] = AddNotificationsToken
