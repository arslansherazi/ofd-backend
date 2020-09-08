from rest_framework import serializers


class DeleteAddressValidator(serializers.Serializer):
    address_id = serializers.IntegerField()
