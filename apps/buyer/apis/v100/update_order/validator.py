from rest_framework import serializers


class MenuItemValidator(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.IntegerField()
    updated_quantity = serializers.IntegerField(required=False)
    is_removed = serializers.BooleanField(required=False, default=False)
    is_changed = serializers.BooleanField(required=False, default=False)


class UpdateOrderValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    delivery_address = serializers.CharField(required=False, max_length=255)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    is_delivery = serializers.BooleanField(required=False, default=False)
    is_takeaway = serializers.BooleanField(required=False, default=False)
    order_items = MenuItemValidator(required=False, many=True)

    def validate(self, attrs):
        if attrs.get('delivery_address'):
            if not attrs.get('latitude'):
                raise ValueError('latitude is required')
            if not attrs.get('longitude'):
                raise ValueError('longitude is required')
        return attrs
