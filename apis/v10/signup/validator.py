from rest_framework import serializers

from common.constants import MERCHANT_USER_TYPE


class SignupValidator(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=100)
    user_type = serializers.IntegerField()
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    image = serializers.ImageField(required=False)
    name = serializers.CharField(required=False, max_length=100)
    title = serializers.CharField(required=False, max_length=255)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    location_id = serializers.IntegerField(required=False)
    contact_no = serializers.CharField(required=False, max_length=100)
    address = serializers.CharField(required=False, max_length=255)
    menus_limit = serializers.IntegerField(required=False)
    items_limit = serializers.IntegerField(required=False)
    is_takeaway_enabled = serializers.BooleanField(required=False, default=False)
    is_delivery_enabled = serializers.BooleanField(required=False, default=False)
    opening_time = serializers.TimeField(required=False)
    closing_time = serializers.TimeField(required=False)
    opening_days = serializers.CharField(required=False, max_length=255)
    is_open_all_day = serializers.BooleanField()
    is_open_all_week = serializers.BooleanField()

    def validate(self, attrs):
        if attrs['user_type'] == MERCHANT_USER_TYPE:
            if not attrs.get('name'):
                raise serializers.ValidationError('name is required')
            if not attrs.get('image'):
                raise serializers.ValidationError('image is required')
            if not attrs.get('latitude'):
                raise serializers.ValidationError('latitude is required')
            if not attrs.get('longitude'):
                raise serializers.ValidationError('longitude is required')
            if not attrs.get('location_id'):
                raise serializers.ValidationError('location_id is required')
            if not attrs.get('contact_no'):
                raise serializers.ValidationError('contact_no is required')
            if not attrs.get('address'):
                raise serializers.ValidationError('address is required')
            if not attrs.get('items_limit'):
                raise serializers.ValidationError('items_limit is required')
            if not attrs.get('menus_limit'):
                raise serializers.ValidationError('menus_limit is required')
            if not attrs.get('is_open_all_day'):
                if not attrs.get('opening_time'):
                    raise serializers.ValidationError('opening_time is required')
                if not attrs.get('closing_time'):
                    raise serializers.ValidationError('closing_time is required')
            if not attrs.get('is_open_all_week'):
                if not attrs.get('opening_days'):
                    raise serializers.ValidationError('opening_days is required')
        else:
            if not attrs.get('first_name'):
                raise serializers.ValidationError('first_name is required')
            if not attrs.get('last_name'):
                raise serializers.ValidationError('last_name is required')
        return attrs
