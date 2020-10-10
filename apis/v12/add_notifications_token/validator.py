from rest_framework import serializers


class AddNotificationsTokenValidator(serializers.Serializer):
    notifications_token = serializers.CharField(required=True)
