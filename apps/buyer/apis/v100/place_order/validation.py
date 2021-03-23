from rest_framework import serializers


class OrderDetailsValidator(serializers.Serializer):
    item_id = serializers.IntegerField()
    price = serializers.IntegerField()
    item_quantity = serializers.IntegerField()
    discount = serializers.IntegerField(required=False, default=0)


class PlaceOrderValidator(serializers.Serializer):
    merchant_id = serializers.IntegerField()
    is_delivery = serializers.BooleanField(required=False, default=False)
    delivery_address = serializers.CharField(required=False, max_length=255)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    order_details = OrderDetailsValidator(many=True)

    def validate(self, attrs):
        if attrs.get('is_delivery'):
            if not attrs.get('delivery_address'):
                raise serializers.ValidationError('delivery_address is required')
            if not attrs.get('latitude'):
                raise serializers.ValidationError('latitude is required')
            if not attrs.get('longitude'):
                raise serializers.ValidationError('longitude is required')
        return attrs
