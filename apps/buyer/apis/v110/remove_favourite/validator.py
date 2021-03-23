from rest_framework import serializers


class RemoveFavouriteValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
