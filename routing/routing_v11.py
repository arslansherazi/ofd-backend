from apis.v11.create_menu.api import CreateMenu
from apis.v11.create_menu_item.api import CreateMenuItem
from apis.v11.delete_menu.api import DeleteMenu
from apis.v11.delete_menu_item.api import DeleteMenuItem
from apis.v11.menu_items_listing.api import MenuItemsListing
from apis.v11.menus_listing.api import MenusListing
from apis.v11.merchant_orders_listing.api import MerchantOrdersListing
from apis.v11.order_details.api import OrderDetailsApi
from apis.v11.update_menu.api import UpdateMenu
from apis.v11.update_menu_item.api import UpdateMenuItem
from apis.v11.update_merchant_availability.api import \
    UpdateMerchantAvailability
from apis.v11.update_order_status.api import UpdateOrderStatus
from routing.routing_v10 import RoutingV10


class RoutingV11(RoutingV10):
    api_version = '11'

    def set_routing_collection(self):
        super().set_routing_collection()
        self.routing_collection['create_menu'] = CreateMenu
        self.routing_collection['create_menu_item'] = CreateMenuItem
        self.routing_collection['menus_listing'] = MenusListing
        self.routing_collection['menu_items_listing'] = MenuItemsListing
        self.routing_collection['merchant_orders_listing'] = MerchantOrdersListing
        self.routing_collection['order_details'] = OrderDetailsApi
        self.routing_collection['update_order_status'] = UpdateOrderStatus
        self.routing_collection['update_menu'] = UpdateMenu
        self.routing_collection['delete_menu'] = DeleteMenu
        self.routing_collection['update_menu_item'] = UpdateMenuItem
        self.routing_collection['delete_menu_item'] = DeleteMenuItem
        self.routing_collection['update_merchant_availability'] = UpdateMerchantAvailability
