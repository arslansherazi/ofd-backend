from django.contrib import admin
from django.urls import include, path

from common.constants import ROUTING_PREFIX
from routing.routing_v10 import RoutingV10
from routing.routing_v11 import RoutingV11
# routing of versions
from routing.routing_v12 import RoutingV12

routing_v10 = RoutingV10().map_routing()
routing_v11 = RoutingV11().map_routing()
routing_v12 = RoutingV12().map_routing()

urlpatterns = [
    path('admin/', admin.site.urls),

    path(ROUTING_PREFIX, include(routing_v10)),
    path(ROUTING_PREFIX, include(routing_v11)),
    path(ROUTING_PREFIX, include(routing_v12))
]
