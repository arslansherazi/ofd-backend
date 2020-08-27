from rest_framework import serializers


class MerchantsValidator(serializers.Serializer):
    location_id = serializers.IntegerField()
    is_delivery = serializers.BooleanField()
    is_takeaway = serializers.BooleanField()
