from django.db import models
from django.db.models import F

from models.buyer import Buyer
from models.merchant import Merchant
from repositories.v11.merchant_repo import MerchantRepository


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default=MerchantRepository.PlACED_ORDER_STATUS, db_index=True)
    price = models.IntegerField()
    discount = models.IntegerField(null=True, default=0)
    is_delivery = models.BooleanField(default=False, db_index=True)
    delivery_address = models.CharField(max_length=255, null=True, default=None)
    latitude = models.FloatField(null=True, default=None)
    longitude = models.FloatField(null=True, default=None)
    address_title = models.CharField(max_length=50)
    is_price_changed = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'order_history'

    @classmethod
    def save_order(
            cls, merchant_id, buyer_id, price, is_delivery, delivery_address, order_number, latitude, longitude,
            discount=0, status='Placed'
    ):
        """
        Saved order into db

        :param int merchant_id: merchant id
        :param int buyer_id: buyer id
        :param int price: buyer id
        :param bool is_delivery: delivery flag
        :param str delivery_address: status
        :param str order_number: order_number
        :param float latitude: latitude
        :param float longitude: longitude
        :param int discount: buyer id
        :param str status: status
        :rtype int
        :returns order id
        """
        order = cls(
            merchant_id=merchant_id, buyer_id=buyer_id, status=status, price=price, discount=discount,
            is_delivery=is_delivery, delivery_address=delivery_address, order_number=order_number, latitude=latitude,
            longitude=longitude
        )
        order.save()
        return order.id

    @classmethod
    def verify_duplicate_order(cls, merchant_id, buyer_id):
        """
        Verifies that either order placed for a merchant or not

        :param int merchant_id: int
        :param int buyer_id: int
        :returns order statuses
        :rtype list
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id, buyer_id=buyer_id)
        orders = _q.values('id', 'status')
        orders_data = []
        if orders:
            for order in orders:
                order_data = {
                    'id': order.get('id'),
                    'status': order.get('status')
                }
                orders_data.append(order_data)
        return orders_data

    @classmethod
    def get_order_status(cls, order_id, merchant_id=None, buyer_id=None):
        """
        Gets order status.

        :param int order_id: order id
        :param int merchant_id: merchant id
        :param int buyer_id: buyer id
        :rtype str
        :return: order status
        """
        _q = cls.objects
        if merchant_id:
            _q = _q.filter(merchant_id=merchant_id)
        if buyer_id:
            _q = _q.filter(buyer_id=buyer_id)
        _q = _q.filter(id=order_id)
        order_status = _q.values('status').first()
        if order_status:
            return order_status.get('status')
        return ''

    @classmethod
    def update_order_status(cls, order_id, status):
        """
        Updates order status

        :param int order_id: order id
        :param str status: status

        :rtype str
        :returns order number
        """
        order = cls.objects.get(id=order_id)
        order.status = status
        order.save()
        return order.order_number

    @classmethod
    def update_orders_price_changed_flag(cls, order_ids, flag=False):
        """
        Updates price changed flag of order if merchant updates any menu item that was participated in any order so that
        buyer can get updated menu item information while re-ordering that item

        :param list order_ids: order ids
        :param bool flag: price changed flag
        """
        _q = cls.objects
        orders = _q.filter(id__in=order_ids)
        orders.update(is_price_changed=flag)

    @classmethod
    def verify_user_orders(cls, buyer_id=None, merchant_id=None):
        """
        Verifies that either user has running orders or not

        :param int buyer_id: buyer id
        :param int merchant_id: merchant id
        :rtype bool
        """
        _q = cls.objects
        if buyer_id:
            _q = _q.filter(buyer_id=buyer_id)
        if merchant_id:
            _q = _q.filter(merchant_id=merchant_id)
        orders = _q.exclude(status__in=[
            MerchantRepository.COMPLETED_ORDER_STATUS, MerchantRepository.REJECTED_ORDER_STATUS,
            MerchantRepository.CANCELLED_ORDER_STATUS
        ])
        if orders:
            return True
        return False

    @classmethod
    def verify_update_order(cls, order_id):
        """
        Verifies that either order can be updated or not

        :param int order_id: order id
        :rtype bool
        """
        _q = cls.objects
        order = _q.filter(
            id=order_id, status__in=[MerchantRepository.PlACED_ORDER_STATUS, MerchantRepository.ACCEPTED_ORDER_STATUS]
        )
        if order:
            return True
        return False

    @classmethod
    def update_order(
            cls, order_id, price=None, discount=None, delivery_address=None, latitude=None, longitude=None,
            is_delivery=False, is_takeaway=False
    ):
        """
        Updates order

        :param int order_id: order id
        :param int price: price
        :param discount discount: discount
        :param str delivery_address: delivery_address
        :param float latitude: latitude
        :param float longitude: longitude
        :param bool is_delivery: is delivery flag
        :param bool is_takeaway: is takeaway flag
        """
        _q = cls.objects
        order = _q.filter(id=order_id)
        if price:
            order.update(price=price)
            order.update(discount=discount)
        if delivery_address:
            order.update(delivery_address=delivery_address, latitude=latitude, longitude=longitude)
        if is_delivery:
            order.update(is_delivery=True)
        elif is_takeaway:
            order.update(is_delivery=False)

    @classmethod
    def get_order_data(cls, order_id):
        """
        Gets order data

        :param int order_id: order id
        :return: order data
        :rtype dict
        """
        _q = cls.objects
        _q = _q.filter(id=order_id)
        order = _q.values(
            'is_price_changed', 'is_delivery', 'delivery_address', 'merchant_id',
            is_takeaway_enabled=F('merchant__is_takeaway_enabled'),
            is_delivery_enabled=F('merchant__is_delivery_enabled'),
            merchant_name=F('merchant__name'), merchant_address=F('merchant__address'),
            merchant_contact_no=F('merchant__contact_no'), merchant_location_id=F('merchant__location_id'),
            merchant_image_url=F('merchant__user__profile_image_url')
        ).first()
        return order

    @classmethod
    def get_order_price(cls, order_id):
        """
        Gets order price

        :param int order_id: order id
        :rtype int
        :return: order price
        """
        _q = cls.objects
        _q = _q.filter(id=order_id)
        order = _q.values('price').first()
        return order.get('price')

    @classmethod
    def change_review_flag(cls, order_id, is_reviewed=False):
        """
        Change review flag of order

        :param int order_id: order id
        :param bool is_reviewed: review flag of order
        """
        order = cls.objects.get(id=order_id)
        order.is_reviewed = is_reviewed
        order.save()
