from rest_framework import serializers


class LocationDetailsValidator(serializers.Serializer):
    place_id = serializers.CharField()
