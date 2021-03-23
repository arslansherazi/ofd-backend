from django.contrib import admin
from django.urls import include, path

from common.constants import ROUTING_PREFIX
from routing.routing_v100 import RoutingV100
from routing.routing_v110 import RoutingV110

# routing of versions
routing_v100 = RoutingV100().map_routing()
routing_v110 = RoutingV110().map_routing()

urlpatterns = [
    path('admin/', admin.site.urls),

    path(ROUTING_PREFIX, include(routing_v100)),
    path(ROUTING_PREFIX, include(routing_v110))
]
