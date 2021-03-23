from rest_framework import serializers


class UpdateAddressValidation(serializers.Serializer):
    address_id = serializers.IntegerField()
    building_address = serializers.CharField(max_length=100, required=False)
    street_address = serializers.CharField(max_length=100, required=False)
    state_address = serializers.CharField(max_length=100, required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    tag = serializers.CharField(max_length=50, required=False)
