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
        if not any([attrs['is_updated'], attrs['is_removed'], attrs['is_added']]):
            raise serializers.ValidationError('ingredient update flag is required')
        if attrs['is_updated'] or attrs['is_deleted']:
            if not attrs['id']:
                raise serializers.ValidationError('ingredient id is required')
        if attrs['is_updated'] or attrs['is_added']:
            if not attrs['name']:
                raise serializers.ValidationError('ingredient name is required')
            if not attrs['quantity']:
                raise serializers.ValidationError('ingredient quantity name is required')
            if not attrs['unit']:
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
