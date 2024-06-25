from rest_framework import serializers


class FavouritesListingValidator(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
