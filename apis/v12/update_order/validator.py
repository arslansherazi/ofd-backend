from rest_framework import serializers


class MenuItemValidator(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    discount = serializers.IntegerField()
    updated_quantity = serializers.IntegerField(required=False)
    is_removed = serializers.IntegerField(required=False)
    is_changed = serializers.IntegerField(required=False)


class UpdateOrderValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    delivery_address = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    is_delivery = serializers.IntegerField(required=False)
    is_takeaway = serializers.IntegerField(required=False)
    order_items = MenuItemValidator(required=False, many=True)

    def validate(self, attrs):
        if attrs['delivery_address']:
            if not attrs['latitude']:
                raise ValueError('latitude is required')
            if not attrs['longitude']:
                raise ValueError('longitude is required')
        return attrs
