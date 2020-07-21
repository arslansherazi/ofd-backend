from rest_framework import serializers


class OrderStatusValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
