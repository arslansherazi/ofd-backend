from rest_framework import serializers

from common.constants import MERCHANT_USER_TYPE


class SignupValidator(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    user_type = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    image = serializers.ImageField(required=False, default=None)
    name = serializers.CharField(required=False)
    title = serializers.CharField(required=False, default=None)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    location_id = serializers.IntegerField(required=False)
    contact_no = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    menus_limit = serializers.IntegerField(required=False)
    items_limit = serializers.IntegerField(required=False)
    is_takeaway_enabled = serializers.BooleanField(required=False, default=False)
    is_delivery_enabled = serializers.BooleanField(required=False, default=False)
    opening_time = serializers.TimeField(required=False, default=None)
    closing_time = serializers.TimeField(required=False, default=None)
    opening_days = serializers.CharField(max_length=255, required=False, default=None)
    is_open_all_day = serializers.IntegerField(required=False)
    is_open_all_week = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if attrs['user_type'] == MERCHANT_USER_TYPE:
            if not attrs['name']:
                raise serializers.ValidationError('name is required')
            if not attrs['image']:
                raise serializers.ValidationError('image is required')
            if not attrs['latitude']:
                raise serializers.ValidationError('latitude is required')
            if not attrs['longitude']:
                raise serializers.ValidationError('longitude is required')
            if not attrs['location_id']:
                raise serializers.ValidationError('location_id is required')
            if not attrs['contact_no']:
                raise serializers.ValidationError('contact_no is required')
            if not attrs['address']:
                raise serializers.ValidationError('address is required')
            if not attrs['items_limit']:
                raise serializers.ValidationError('items_limit is required')
            if not attrs['menus_limit']:
                raise serializers.ValidationError('menus_limit is required')
            if not attrs['is_open_all_day']:
                if not attrs['opening_time']:
                    raise serializers.ValidationError('opening_time is required')
                if not attrs['closing_time']:
                    raise serializers.ValidationError('closing_time is required')
            if not attrs['is_open_all_week']:
                if not attrs['opening_days']:
                    raise serializers.ValidationError('opening_days is required')
        else:
            if not attrs['first_name']:
                raise serializers.ValidationError('first_name is required')
            if not attrs['last_name']:
                raise serializers.ValidationError('last_name is required')
        return attrs
