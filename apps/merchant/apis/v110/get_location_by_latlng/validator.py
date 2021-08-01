from rest_framework import serializers


class GetLocationBylatLngValidator(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
