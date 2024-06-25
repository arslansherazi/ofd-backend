from rest_framework import serializers


class LocationSuggestionValidator(serializers.Serializer):
    query = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    radius = serializers.IntegerField()
