from rest_framework import serializers


class UpdateMerchantAvailabilityValidator(serializers.Serializer):
    opening_time = serializers.TimeField(required=False)
    closing_time = serializers.TimeField(required=False)
    opening_days = serializers.CharField(required=False, max_length=255)
    is_open_all_day = serializers.IntegerField(required=False)
    is_open_all_week = serializers.IntegerField(required=False)
