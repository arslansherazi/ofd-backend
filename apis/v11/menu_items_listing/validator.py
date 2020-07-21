from rest_framework import serializers


class MenuItemsListingValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
    merchant_id = serializers.IntegerField(required=False)
    is_buyer = serializers.IntegerField()
