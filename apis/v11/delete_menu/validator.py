from rest_framework import serializers


class DeleteMenuValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
