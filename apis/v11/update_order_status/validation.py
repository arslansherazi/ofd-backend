from rest_framework import serializers

from repositories.v11.merchant_repo import MerchantRepository


class DriverInfoValidator(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    vehicle_model = serializers.CharField()
    vehicle_number = serializers.CharField()
    contact_no = serializers.IntegerField()


class UpdateOrderStatusValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()
    status = serializers.CharField()
    driver_info = DriverInfoValidator(required=False)

    def validate(self, attrs):
        if attrs['status'] == MerchantRepository.ON_ROUTE_ORDER_STATUS:
            if not attrs['driver_info']:
                raise serializers.ValidationError('driver_info is required')
        return attrs
