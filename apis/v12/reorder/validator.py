from rest_framework import serializers


class ItemDetailsValidator(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    updated_quantity = serializers.IntegerField(required=False)
    price = serializers.IntegerField()
    discount = serializers.IntegerField()
    is_removed = serializers.IntegerField()
    is_changed = serializers.IntegerField()


class ReorderValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    is_price_checked = serializers.IntegerField()
    is_changed = serializers.IntegerField(required=False)
    is_price_changed = serializers.IntegerField(required=False)
    merchant_id = serializers.IntegerField(required=False)
    merchant_name = serializers.CharField(required=False)
    items_details = ItemDetailsValidator(many=True, required=False)
    is_delivery = serializers.IntegerField(required=False)
    is_takeaway = serializers.IntegerField(required=False)
    delivery_address = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    def validate(self, attrs):
        if attrs['is_price_checked']:
            if not attrs['merchant_id']:
                raise serializers.ValidationError('merchant_id is required')
            if not attrs['merchant_name']:
                raise serializers.ValidationError('merchant_name is required')
        if not attrs['is_price_checked']:
            if not attrs['is_price_changed']:
                if not attrs['is_changed']:
                    raise serializers.ValidationError('is_changed is required')
            if not attrs['items_details']:
                raise serializers.ValidationError('items_details is required')
        return attrs
