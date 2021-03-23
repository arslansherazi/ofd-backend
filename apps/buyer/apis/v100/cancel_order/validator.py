from rest_framework import serializers


class CancelOrderValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
