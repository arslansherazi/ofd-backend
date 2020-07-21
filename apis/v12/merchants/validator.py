from rest_framework import serializers


class MerchantsValidator(serializers.Serializer):
    location_id = serializers.IntegerField()
    is_delivery = serializers.IntegerField()
    is_takeaway = serializers.IntegerField()
