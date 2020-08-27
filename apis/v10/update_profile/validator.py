from rest_framework import serializers


class UpdateProfileValidator(serializers.Serializer):
    user_type = serializers.IntegerField()
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    profile_image = serializers.ImageField(required=False)
    name = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    contact_no = serializers.IntegerField(required=False)
    address = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    is_delivery_enabled = serializers.BooleanField(required=False)
    is_takeaway_enabled = serializers.BooleanField(required=False)
