from rest_framework import serializers


class MerchantOrdersListingFiltersValidator(serializers.Serializer):
    menu_id = serializers.IntegerField(required=False)
    date = serializers.DateField(required=False)
    order_number = serializers.CharField(required=False, max_length=50)
    buyer_name = serializers.CharField(required=False, max_length=150)
    buyer_address = serializers.CharField(required=False, max_length=255)


class MerchantOrdersListingValidator(serializers.Serializer):
    # filters = MerchantOrdersListingFiltersValidator(required=False, default={})
    filters = serializers.CharField(required=False, default='{}')
    offset = serializers.IntegerField(required=False, default=0)
    limit = serializers.IntegerField(required=False, default=20)
