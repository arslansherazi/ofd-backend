from rest_framework import serializers


class DeleteMenuItemValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
