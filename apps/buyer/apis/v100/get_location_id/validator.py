from rest_framework import serializers


class GetLocationIdValidator(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
