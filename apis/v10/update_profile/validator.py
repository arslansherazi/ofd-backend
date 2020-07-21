from rest_framework import serializers


class UpdateProfileValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
    username = serializers.CharField(required=False, default=None)
    first_name = serializers.CharField(required=False, default=None)
    last_name = serializers.CharField(required=False, default=None)
    profile_image = serializers.ImageField(required=False, default=None)
    name = serializers.CharField(required=False, default=None)
    title = serializers.CharField(required=False, default=None)
    contact_no = serializers.IntegerField(required=False, default=None)
    address = serializers.CharField(required=False, default=None)
    latitude = serializers.FloatField(required=False, default=None)
    longitude = serializers.FloatField(required=False, default=None)
    is_delivery_enabled = serializers.BooleanField(required=False, default=False)
    is_takeaway_enabled = serializers.BooleanField(required=False, default=False)
