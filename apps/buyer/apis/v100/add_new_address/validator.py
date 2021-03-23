from rest_framework import serializers


class AddNewAddressValidator(serializers.Serializer):
    building_address = serializers.CharField(max_length=100, required=False)
    street_address = serializers.CharField(max_length=100)
    state_address = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    tag = serializers.CharField(max_length=50)
