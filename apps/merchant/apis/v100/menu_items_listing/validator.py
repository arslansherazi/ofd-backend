from rest_framework import serializers


class MenuItemsListingValidator(serializers.Serializer):
    menu_id = serializers.IntegerField()
    merchant_id = serializers.IntegerField(required=False)
    is_buyer = serializers.BooleanField()
    menu_item_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        if attrs.get('is_buyer'):
            if not attrs.get('menu_item_id'):
                raise serializers.ValidationError('menu_item_id is required')
        return attrs
