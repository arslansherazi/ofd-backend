from rest_framework import serializers


class IngredientValidator(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False, max_length=100)
    quantity = serializers.IntegerField(required=False)
    unit = serializers.CharField(required=False, max_length=50)
    is_updated = serializers.BooleanField(required=False, default=False)
    is_removed = serializers.BooleanField(required=False, default=False)
    is_added = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        if not any([attrs.get('is_updated'), attrs.get('is_removed'), attrs.get('is_added')]):
            raise serializers.ValidationError('ingredient update flag is required')
        if attrs.get('is_updated') or attrs.get('is_deleted'):
            if not attrs['id']:
                raise serializers.ValidationError('ingredient id is required')
        if attrs.get('is_updated') or attrs.get('is_added'):
            if not attrs.get('name'):
                raise serializers.ValidationError('ingredient name is required')
            if not attrs.get('quantity'):
                raise serializers.ValidationError('ingredient quantity name is required')
            if not attrs.get('unit'):
                raise serializers.ValidationError('ingredient unit is required')
        return attrs


class UpdateMenuItemValidator(serializers.Serializer):
    menu_item_id = serializers.IntegerField()
    name = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    quantity = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)
    discount = serializers.IntegerField(required=False)
    is_activated = serializers.BooleanField(required=False, default=False)
    is_deactivated = serializers.BooleanField(required=False, default=False)
    ingredients = IngredientValidator(many=True, required=False)
