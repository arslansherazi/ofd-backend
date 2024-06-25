from rest_framework import serializers


class UpdateProfileValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
    username = serializers.CharField(required=False, max_length=100)
    first_name = serializers.CharField(required=False, max_length=50)
    last_name = serializers.CharField(required=False, max_length=50)
    profile_image = serializers.ImageField(required=False)
    name = serializers.CharField(required=False, max_length=100)
    title = serializers.CharField(required=False, max_length=255)
    contact_no = serializers.IntegerField(required=False, max_value=100)
    address = serializers.CharField(required=False, max_length=255)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    is_delivery_enabled = serializers.BooleanField(required=False)
    is_takeaway_enabled = serializers.BooleanField(required=False)
