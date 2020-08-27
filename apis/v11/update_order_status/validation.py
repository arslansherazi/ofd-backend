from rest_framework import serializers

from repositories.v11.merchant_repo import MerchantRepository


class DriverInfoValidator(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    vehicle_model = serializers.CharField(max_length=50)
    vehicle_number = serializers.CharField(max_length=50)
    contact_no = serializers.IntegerField()


class UpdateOrderStatusValidator(serializers.Serializer):
    order_id = serializers.IntegerField()
    buyer_id = serializers.IntegerField()
    status = serializers.CharField(max_length=50)
    driver_info = DriverInfoValidator(required=False)

    def validate(self, attrs):
        if attrs['status'] == MerchantRepository.ON_ROUTE_ORDER_STATUS:
            if not attrs['driver_info']:
                raise serializers.ValidationError('driver_info is required')
        return attrs
