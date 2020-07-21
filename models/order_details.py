from django.db import models
from django.db.models import F, Q, Value
from django.db.models.functions import Concat

from common.common_helpers import CommonHelpers
from models.menu_item import MenuItem
from models.order import Order
from repositories.v11.merchant_repo import MerchantRepository


class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    item_quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'order_details'

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
                item_quantity=order_detail.get('item_quantity')
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
            _q = _q.select_related('buyer')
            buyer_first_name = buyer_name.split(' ')[0].lower()
            buyer_last_name = buyer_name.split(' ')[-1].lower()
            _q = _q.filter(
                Q(order__buyer__first_name__icontains=buyer_first_name) |
                Q(order__buyer__last_name__icontains=buyer_last_name)
            )
        if is_delivery:
            _q = _q.filter(order__is_delivery=True)
            if delivery_address:
                _q = _q.filter(order__delivery_address__contains=delivery_address.lower())
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
        _q = cls.objects
        _q = _q.select_related('order', 'item', 'merchant')
        _q = _q.filter(order_id=order_id, order__buyer_id=buyer_id, order__merchant_id=merchant_id)
        # if buyer_order_details:
        #     _q = _q.values(
        #         merchant_name=F('item__merchant__name'), contact_no=F('item__merchant__contact_no')
        #     )
        order_details = _q.values(
            'id', 'order_id', 'item_id', 'item_quantity', order_number=F('order__order_number'),
            status=F('order__status'), price=F('order__price'), discount=F('order__discount'),
            is_delivery=F('order__is_delivery'), delivery_address=F('order__delivery_address'), name=F('item__name'),
            unit=F('item__unit'), quantity=F('item__quantity'), item_price=F('item__price'),
            item_rating=F('item__rating'), item_discount=F('item__discount'),
            buyer_name=Concat('order__buyer__first_name', Value(' '), 'order__buyer__last_name'),
            merchant_name=F('item__merchant__name'), merchant_contact_no=F('item__merchant__contact_no')
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
        return menu_item_orders_ids

    @classmethod
    def delete_order_items(cls, order_id, order_details_ids):
        """
        Deletes order items

        :param int order_id: order id
        :param list order_details_ids: menu items ids
        """
        _q = cls.objects
        order_items = _q.filter(id__in=order_details_ids)
        order_items.delete()

    @classmethod
    def update_order_items(cls, order_id, updated_items):
        """
        Updates order items

        :param int order_id: order id
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
        order_items_details = _q.values(
            'id', quantity=F('item_quantity'), name=F('item__name'), unit=F('item__unit'),
            unit_quantity=F('item__quantity'), price=F('item__price'), discount=F('item__discount')
        )
        return order_items_details
