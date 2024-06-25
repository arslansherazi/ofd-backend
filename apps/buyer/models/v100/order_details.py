from django.core.cache import cache
from django.db import models
from django.db.models import F, Q, Value
from django.db.models.functions import Concat

from apps.buyer.models.v100.order import Order
from apps.merchant.models.v100.menu_item import MenuItem
from apps.merchant.repositories.v100.merchant_repo import MerchantRepository
from common.common_helpers import CommonHelpers


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    item_quantity = models.IntegerField()
    item_price = models.IntegerField()
    item_discount = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'buyer'
        db_table = 'order_details'

    @classmethod
    def get_buyer_orders(cls, buyer_id=None, order_id=None):
        """
        Gets all orders of buyer

        :param int buyer_id: buyer id
        :param int order_id: order id
        :rtype list
        :returns orders list
        """
        _q = cls.objects
        _q = _q.select_related('merchant', 'order')
        if buyer_id:
            _q = _q.filter(order__buyer_id=buyer_id)
        else:
            _q = _q.filter(order_id=order_id)
        _q = _q.order_by(F('order__updated_date').desc())
        orders_data = _q.values(
            'id', 'order_id', status=F('order__status'), order_number=F('order__order_number'),
            is_delivery=F('order__is_delivery'), delivery_address=F('order__delivery_address'),
            merchant_name=F('order__merchant__name'), merchant_address=F('order__merchant__address'),
            order_item_id=F('item_id'), order_item_quantity=F('item_quantity'), order_item_name=F('item__name'),
            order_item_price=F('item_price'), order_item_discount=F('item_discount'), order_price=F('order__price'),
            order_date=F('order__created_date'), merchant_id=F('order__merchant__id'),
            is_reviewed=F('order__is_reviewed'), merchant_latitude=F('order__merchant__latitude'),
            merchant_longitude=F('order__merchant__longitude'), latitude=F('order__latitude'),
            longitude=F('order__longitude')
        )
        orders = {}
        for order_data in orders_data:
            order_id = order_data.get('order_id')
            if order_id in orders:
                order_item = {
                    'id': order_data.get('id'),
                    'item_id': order_data.get('order_item_id'),
                    'item_name': order_data.get('order_item_name'),
                    'item_quantity': order_data.get('order_item_quantity'),
                    'price': order_data.get('order_item_price'),
                    'discount': order_data.get('order_item_discount')
                }
                orders[order_id]['order_items'].append(order_item)
            else:
                orders[order_id] = {
                    'id': order_id,
                    'status': order_data.get('status'),
                    'order_number': order_data.get('order_number'),
                    'price': order_data.get('order_price'),
                    'is_delivery': bool(order_data.get('is_delivery')),
                    'delivery_address': order_data.get('delivery_address'),
                    'merchant_name': order_data.get('merchant_name'),
                    'merchant_address': order_data.get('merchant_address'),
                    'merchant_id': order_data.get('merchant_id'),
                    'date': order_data.get('order_date').strftime('%m/%d/%Y, %H:%M:%S'),
                    'is_reviewed': order_data.get('is_reviewed'),
                    'order_items': [{
                        'id': order_data.get('id'),
                        'item_id': order_data.get('order_item_id'),
                        'item_name': order_data.get('order_item_name'),
                        'item_quantity': order_data.get('order_item_quantity'),
                        'price': order_data.get('order_item_price'),
                        'discount': order_data.get('order_item_discount')
                    }]
                }
                if (
                        order_data.get('is_delivery', False) and
                        order_data.get('status').lower() not in ['cancelled', 'completed']
                ):
                    orders[order_id]['average_delivery_time'] = CommonHelpers.calculate_delivery_time_and_distance(
                        latitude=order_data.get('latitude'), longitude=order_data.get('longitude'),
                        merchant_latitude=order_data.get('merchant_latitude'),
                        merchant_longitude=order_data.get('merchant_longitude'),
                        is_delivery=True
                    )
        if buyer_id:
            return list(orders.values())
        else:
            return orders.get(order_id, {})

    @classmethod
    def save_order_details(cls, order_id, order_details):
        """
        Saves order details

        :param int order_id: order id
        :param list order_details: order details
        """
        order_details_objects = []
        for order_detail in order_details:
            order_detail_object = cls(
                order_id=order_id,
                item_id=order_detail.get('item_id'),
                item_quantity=order_detail.get('item_quantity'),
                item_price=order_detail.get('price'),
                item_discount=order_detail.get('discount')
            )
            order_details_objects.append(order_detail_object)
        cls.objects.bulk_create(order_details_objects)

    @classmethod
    def get_merchant_orders(cls, merchant_id, **kwargs):
        """
        Gets orders of merchant. It applies filters on orders if available

        :param int merchant_id: merchant id
        :param kwargs: filters
        :rtype list
        :return: orders
        """
        menu_id = kwargs.get('menu_id', None)
        date = kwargs.get('date', None)
        order_number = kwargs.get('order_number', None)
        buyer_name = kwargs.get('buyer_name', None)
        delivery_address = kwargs.get('delivery_address', None)
        is_delivery = kwargs.get('is_delivery', None)
        is_takeaway = kwargs.get('is_takeaway', None)

        _q = cls.objects
        _q = _q.select_related('order')
        if menu_id:
            _q = _q.select_related('item', 'menu')
            _q = _q.filter(item__menu__id=menu_id)
        if date:
            start_time = '{} 00:00:00'.format(date)
            end_time = '{} 23:59:59'.format(date)
            _q = _q.filter(order__created_date__range=(start_time, end_time))
        if order_number:
            _q = _q.filter(order__order_number=order_number)
        if buyer_name:
            _q = _q.annotate(
                buyer_search_name=Concat('order__buyer__first_name', Value(' '), 'order__buyer__last_name')
            )
            _q = _q.filter(
                buyer_search_name__icontains=buyer_name
            )
        if is_delivery:
            _q = _q.filter(order__is_delivery=True)
            if delivery_address:
                _q = _q.filter(order__delivery_address__icontains=delivery_address.lower())
        if is_takeaway:
            _q = _q.filter(order__is_delivery=False)
        _q = _q.filter(order__merchant_id=merchant_id)
        orders = _q.values(
            'order_id', buyer_id=F('order__buyer_id'), order_number=F('order__order_number'),
            is_delivery=F('order__is_delivery'), delivery_address=F('order__delivery_address'),
            status=F('order__status'),
            buyer_name=Concat('order__buyer__first_name', Value(' '), 'order__buyer__last_name'),
        ).distinct()
        for order in orders:
            delivery_address = order.get('delivery_address', '')
            buyer_name = order.get('buyer_name', '')
            if delivery_address:
                order['delivery_address'] = CommonHelpers.capitalize_string(delivery_address)
            order['buyer_name'] = CommonHelpers.capitalize_string(buyer_name)
        return orders

    @classmethod
    def get_order_details(
            cls, order_id, merchant_id, buyer_id, buyer_order_details=False
    ):
        """
        Gets order details

        :param int order_id: order id
        :param int merchant_id: merchant id
        :param int buyer_id: buyer id
        :param bool buyer_order_details: buyer order details flag
        :rtype list
        :return: order details
        """
        columns = {}
        _q = cls.objects
        _q = _q.select_related('order', 'item', 'merchant')
        _q = _q.filter(order_id=order_id, order__buyer_id=buyer_id, order__merchant_id=merchant_id)
        if buyer_order_details:
            columns = {
                'merchant_name': F('item__merchant__name'),
                'contact_no': F('item__merchant__contact_no')
            }
        order_details = _q.values(
            'id', 'order_id', 'item_id', 'item_quantity', order_number=F('order__order_number'),
            status=F('order__status'), price=F('order__price'), discount=F('order__discount'),
            is_delivery=F('order__is_delivery'), delivery_address=F('order__delivery_address'), name=F('item__name'),
            unit=F('item__unit'), quantity=F('item__quantity'), item_price=F('item__price'),
            item_rating=F('item__rating'), item_discount=F('item__discount'),
            buyer_name=Concat('order__buyer__first_name', Value(' '), 'order__buyer__last_name'),
            **columns
        )
        return order_details

    @classmethod
    def verify_menu_items_orders(cls, menu_id, merchant_id):
        """
        Verifies that either items in the merchant menu participates in running orders or not

        :param int menu_id: menu id
        :param int merchant_id: merchant id
        :rtype bool
        """
        _q = cls.objects
        _q = _q.select_related('order', 'item')
        _q = _q.exclude(order__status__in=[
            MerchantRepository.COMPLETED_ORDER_STATUS, MerchantRepository.CANCELLED_ORDER_STATUS,
            MerchantRepository.REJECTED_ORDER_STATUS
        ])
        menu_items_orders = _q.filter(order__merchant__id=merchant_id, item__menu__id=menu_id)
        if menu_items_orders:
            return True
        return False

    @classmethod
    def verify_menu_item_orders(cls, menu_item_id):
        """
        Verifies that either menu item participates in running orders or not

        :param int menu_item_id: menu item id
        :rtype bool
        """
        _q = cls.objects
        _q = _q.select_related('item', 'order')
        _q = _q.filter(item__id=menu_item_id)
        menu_item_orders = _q.exclude(order__status__in=[
            MerchantRepository.COMPLETED_ORDER_STATUS, MerchantRepository.CANCELLED_ORDER_STATUS,
            MerchantRepository.REJECTED_ORDER_STATUS
        ])
        if menu_item_orders:
            return True
        return False

    @classmethod
    def get_menu_item_orders_ids(cls, menu_item_id):
        """
        Gets ids of menu item orders

        :param int menu_item_id: menu item id
        :rtype list
        :returns menu item orders ids
        """
        cache_key = 'OrderDetails:get_menu_item_orders_ids:{}'.format(menu_item_id)
        cache_value = cache.get(cache_key)
        if cache_value:
            return cache_value
        _q = cls.objects
        _q = _q.select_related('item', 'order')
        _q = _q.filter(item__id=menu_item_id, order__status__in=[
            MerchantRepository.COMPLETED_ORDER_STATUS, MerchantRepository.CANCELLED_ORDER_STATUS,
            MerchantRepository.REJECTED_ORDER_STATUS
        ])
        menu_item_orders_data = _q.values('order_id')
        menu_item_orders_ids = []
        for menu_item_order_data in menu_item_orders_data:
            menu_item_order_id = menu_item_order_data.get('order_id')
            menu_item_orders_ids.append(menu_item_order_id)
        cache.set(cache_key, menu_item_orders_ids)
        return menu_item_orders_ids

    @classmethod
    def delete_order_items(cls, order_details_ids):
        """
        Deletes order items

        :param list order_details_ids: menu items ids
        """
        _q = cls.objects
        order_items = _q.filter(id__in=order_details_ids)
        order_items.delete()

    @classmethod
    def update_order_items(cls, updated_items):
        """
        Updates order items

        :param list updated_items: updated order items
        """
        updated_order_items = []
        for updated_item in updated_items:
            updated_order_detail_id = updated_item.get('id')
            order_item = cls.objects.get(id=updated_order_detail_id)
            order_item.item_quantity = updated_item.get('updated_quantity')
            updated_order_items.append(order_item)
        cls.objects.bulk_update(updated_order_items, ['item_quantity'])

    @classmethod
    def verify_buyer_order_items(cls, buyer_id, order_id, items_ids):
        """
        Verifies that either items exist against the order

        :param int buyer_id: buyer id
        :param int order_id: order id
        :param list items_ids: items ids
        :rtype bool
        """
        _q = cls.objects
        _q = _q.select_related('order')
        order_items = _q.filter(item_id__in=items_ids, order_id=order_id, order__buyer_id=buyer_id)
        if order_items:
            return True
        return False

    @classmethod
    def get_order_items_details(cls, order_id):
        """
        Gets details of order items

        :param int order_id: order id
        """
        _q = cls.objects
        _q = _q.select_related('item')
        _q = _q.filter(order_id=order_id, item__is_active=True)
        order_items_details_data = _q.values(
            'item_id', 'item_quantity', order_item_id=F('id'), name=F('item__name'), price=F('item__price'),
            discount=F('item__discount'), image_url=F('item__image_url')
        )
        for order_items_details in order_items_details_data:
            order_items_details['is_selected'] = True
            order_items_details['id'] = order_items_details.get('item_id')
        return order_items_details_data
