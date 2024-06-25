from rest_framework import serializers


class OrderDetailsValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField(required=False)
    merchant_id = serializers.IntegerField(required=False)
