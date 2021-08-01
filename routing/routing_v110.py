from apps.buyer.apis.v110.add_favourite.api import AddFavourite
from apps.buyer.apis.v110.favourites_listing.api import FavouritesListing
from apps.buyer.apis.v110.remove_favourite.api import RemoveFavourite
from apps.buyer.apis.v110.view_all_items.api import ViewAllItems
from apps.merchant.apis.v110.get_location_by_latlng.api import GetLocationByLatLng
from apps.merchant.apis.v110.location_details.api import LocationDetails
from apps.merchant.apis.v110.location_suggestion.api import LocationSuggestions
from apps.merchant.apis.v110.report.api import ReportApi
from apps.user.apis.v110.update_profile.api import UpdateProfile
from routing.routing_v100 import RoutingV100


class RoutingV110(RoutingV100):
    api_version = '110'

    def set_routing_collection(self):
        super().set_routing_collection()
        self.routing_collection['update_profile'] = UpdateProfile
        self.routing_collection['add_favourite'] = AddFavourite
        self.routing_collection['remove_favourite'] = RemoveFavourite
        self.routing_collection['favourites_listing'] = FavouritesListing
        self.routing_collection['report'] = ReportApi
        self.routing_collection['view_all_items'] = ViewAllItems
        self.routing_collection['location_suggestions'] = LocationSuggestions
        self.routing_collection['location_details'] = LocationDetails
        self.routing_collection['get_location_by_latlng'] = GetLocationByLatLng
