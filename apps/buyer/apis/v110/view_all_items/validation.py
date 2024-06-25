from rest_framework import serializers


class ViewAllItemsValidator(serializers.Serializer):
    location_id = serializers.IntegerField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    is_takeaway = serializers.BooleanField(required=False)
    is_delivery = serializers.BooleanField(required=False)
    is_discounted = serializers.BooleanField(required=False, default=False)
    is_top_rated = serializers.BooleanField(required=False, default=False)
    is_nearby = serializers.BooleanField(required=False, default=False)
    is_merchant = serializers.BooleanField(required=False, default=False)
    merchant_id = serializers.IntegerField(required=False)
    menu_id = serializers.IntegerField(required=False)
    limit = serializers.IntegerField(required=False, default=10)
    offset = serializers.IntegerField()

    def validate(self, attrs):
        if not attrs.get('is_merchant'):
            if not attrs.get('location_id'):
                serializers.ValidationError('location_id is required')
            elif not attrs.get('latitude'):
                serializers.ValidationError('latitude is required')
            elif not attrs.get('longitude'):
                serializers.ValidationError('longitude is required')
            elif not attrs.get('is_takeaway'):
                serializers.ValidationError('is_takeaway is required')
            elif not attrs.get('is_delivery'):
                serializers.ValidationError('is_delivery is required')
        else:
            if not attrs.get('merchant_id'):
                serializers.ValidationError('merchant_id is required')
            elif not attrs.get('menu_id'):
                serializers.ValidationError('menu_id is required')
        return attrs
