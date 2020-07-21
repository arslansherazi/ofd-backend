from rest_framework import serializers


class MerchantOrdersListingFiltersValidator(serializers.Serializer):
    menu_id = serializers.IntegerField(required=False, default=None)
    date = serializers.DateField(required=False, default=None)
    order_number = serializers.CharField(required=False, default=None)
    buyer_name = serializers.CharField(required=False, default=None)
    buyer_address = serializers.CharField(required=False, default=False)


class MerchantOrdersListingValidator(serializers.Serializer):
    filters = MerchantOrdersListingFiltersValidator(required=False)
    offset = serializers.IntegerField(required=False, default=0)
    limit = serializers.IntegerField(required=False, default=20)
