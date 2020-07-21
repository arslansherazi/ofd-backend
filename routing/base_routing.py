from django.urls import path


class BaseRouting(object):
    routing_collection = {}
    api_version = ''

    def set_routing_collection(self):
        pass

    def set_routing(self):
        routing = []
        for api_endpoint, api_class in self.routing_collection.items():
            api_endpoint_path = 'v{api_version}/{api_endpoint}'.format(
                api_version=self.api_version, api_endpoint=api_endpoint
            )
            api_path = path(api_endpoint_path, api_class.as_view())
            routing.append(api_path)
        return routing

    def map_routing(self):
        self.set_routing_collection()
        return self.set_routing()
