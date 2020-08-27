from rest_framework import serializers


class ItemsListingValidator(serializers.Serializer):
    query = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_takeaway = serializers.BooleanField()
    is_delivery = serializers.BooleanField()
    offset = serializers.IntegerField()
    is_auto_suggest_items = serializers.BooleanField(required=False, default=False)
