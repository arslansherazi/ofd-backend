from rest_framework import serializers


class ItemsListingValidator(serializers.Serializer):
    # query = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_takeaway = serializers.IntegerField()
    is_delivery = serializers.IntegerField()
    offset = serializers.IntegerField()
    is_auto_suggest_items = serializers.IntegerField(required=False, default=0)
