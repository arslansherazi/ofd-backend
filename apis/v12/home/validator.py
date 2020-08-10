from rest_framework import serializers


class HomeValidator(serializers.Serializer):
    location_id = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_takeaway = serializers.IntegerField()
    is_delivery = serializers.IntegerField()
