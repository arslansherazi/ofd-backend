from collections import defaultdict

import geopy.distance

from common.constants import AVERAGE_PREPARATION_TIME, BUFFER_TIME
from models.order import Order
from models.order_details import OrderDetails


class BuyerRepository(object):
    """
    Buyer Repository
    """
    DUPLICATE_ORDER_MESSAGE = 'An order is already placed. {}'
    EDITABLE_ORDER_MESSAGE = 'You can edit the order'
    EDITABLE_ORDER_STATUSES = ['Placed', 'Accepted']
    NO_ORDER_TITLE = 'You have not make any orders(s) yet.'
    NO_ORDER_MESSAGE = 'Your orders will appear here as you make orders in the app'
    FEEDBACK_SUCCESS_MESSAGE = 'Thank you for your feedback.'
    UPDATE_ORDER_ERROR_MESSAGE = 'Order cannot be updated'
    UPDATE_ORDER_SUCCESS_MESSAGE = 'Order is updated successfully'
    FEEDBACK_ERROR_MESSAGE = 'Order doest not exist or does not contain these items'
    REORDER_PRICE_CHANGE_MESSAGE = '{} has changed some of the items in your order. Price may be changed.'
    DISCOUNTED_SECTION_NAME = 'Top Discount'
    TOP_RATED_SECTION_NAME = 'Top Rated'
    NEARBY_SECTION_NAME = 'Nearby'
    HOME_SECTIONS_ITEMS_LIMIT = 5
    NO_ITEMS_FOUND_MESSAGE = 'No results found. Please try changing your search criteria.'
    NO_ITEMS_FOUND_TITLE = 'Uh Oh!'
    FAVOURITES_LIMIT_EXCEEDS_MESSAGE = 'Sorry. You can add only 10 favourites'
    NO_FAVOURITES_TITLE = 'No Favourites'
    NO_FAVOURITES_MESSAGE = 'You have not make any favourites yet'
    NO_FAVOURITES_IMAGE_NAME = 'no_favourites.png'
    FAVOURITES_LIMIT = 10
    NO_FAVOURITES_COUNT = 0
    FAVOURITE_NOT_EXISTS_MESSAGE = 'Favourite does not exists'
    NO_ORDERS_IMAGE_NAME = 'no_orders.png'
    OUT_OF_REACH_TITLE = 'Out of our reach'
    OUT_OF_REACH_MESSAGE = 'Sorry, Seems like your address is outside of our service area'
    ADDRESS_LIMIT_EXCEEDS_MESSAGE = 'You can save only {} addresses'
    ADDRESS_ALREADY_PRESENT_MESSAGE = 'Address already present with {} tag'

    @staticmethod
    def update_order(
            order_id, items_details, delivery_address=None, latitude=None, longitude=None, is_delivery=False,
            is_takeaway=False
    ):
        """
        Updates order

        1. Updates order items quantity
        2. Deletes order items
        3. Calculates order new price
        4. Calculates order new discount

        :param int order_id: order id
        :param list items_details: order items details
        :param str delivery_address: delivery address
        :param float latitude: latitude
        :param float longitude: longitude
        :param bool is_delivery: is delivery flag
        :param bool is_takeaway: is takeaway flag
        """
        order_new_price = 0
        order_new_discounted_price = 0
        deleted_order_details_ids = []
        updated_items = []
        for menu_item in items_details:
            order_details_id = menu_item.get('id')
            menu_item_price = menu_item.get('price')
            menu_item_discount = menu_item.get('discount')
            if menu_item.get('is_removed', False):
                deleted_order_details_ids.append(order_details_id)
            elif menu_item.get('is_changed', False):
                menu_item_updated_quantity = menu_item.get('updated_quantity')
                updated_menu_item = {
                    'id': order_details_id,
                    'updated_quantity': menu_item_updated_quantity
                }
                updated_items.append(updated_menu_item)
                total_price = menu_item_price * menu_item_updated_quantity
                order_new_price += total_price
                order_new_discounted_price = order_new_discounted_price + ((order_new_price / 100) * menu_item_discount)
            else:
                menu_item_quantity = menu_item.get('quantity')
                total_price = menu_item_price * menu_item_quantity
                order_new_price += total_price
        discount = round(((order_new_price - (order_new_price - order_new_discounted_price)) / order_new_price) * 100)
        if deleted_order_details_ids:
            OrderDetails.delete_order_items(order_id, deleted_order_details_ids)
        if updated_items:
            OrderDetails.update_order_items(order_id, updated_items)

        if any([order_new_price, delivery_address, is_delivery, is_takeaway]):
            updated_columns = {}
            if order_new_price:
                updated_columns.update(price=order_new_price, discount=discount)
            if delivery_address:
                updated_columns.update(
                    delivery_address=delivery_address, latitude=latitude, longitude=longitude
                )
            if is_delivery:
                updated_columns.update(is_delivery=True)
            elif is_takeaway:
                updated_columns.update(is_takeaway=True)
            Order.update_order(order_id=order_id, **updated_columns)

    @staticmethod
    def calculate_distance_btw_buyer_and_merchant(latitude, longitude, merchants, is_takeaway, is_delivery):
        """
        Calculates distance between buyer and merchant

        :param float latitude: buyer latitude
        :param float longitude: buyer longitude
        :param list merchants: merchants
        :param bool is_takeaway: takeaway flag
        :param bool is_delivery: delivery flag
        :rtype list
        :return: merchants after calculating distance
        """
        for merchant in merchants:
            merchant_latitude = merchant.get('merchant_info').get('latitude')
            merchant_longitude = merchant.get('merchant_info').get('longitude')
            merchant_location = (merchant_latitude, merchant_longitude)
            buyer_location = (latitude, longitude)
            distance = geopy.distance.vincenty(merchant_location, buyer_location).km
            distance_unit = 'km'
            if is_delivery:
                delivery_time = round(distance + AVERAGE_PREPARATION_TIME + BUFFER_TIME)
                if delivery_time <= 60:
                    merchant['delivery_time_with_unit'] = '{} MIN'.format(delivery_time)
                else:
                    delivery_time_hours = delivery_time // 60
                    delivery_time_minutes = delivery_time % 60
                    merchant['delivery_time_with_unit'] = '{hours} HRS {minutes} MIN'.format(
                        hours=delivery_time_hours, minutes=delivery_time_minutes
                    )
                merchant['delivery_time'] = delivery_time
            if is_takeaway:
                if not distance >= 1:
                    distance = distance * 1000
                    distance_unit = 'm'
                distance = round(distance, 2)
                merchant['distance'] = distance
                merchant['distance_with_unit'] = '{distance} {unit}'.format(
                    distance=distance, unit=distance_unit
                )
        return merchants

    @staticmethod
    def get_distinct_merchants_items(items):
        """
        Gets distinct merchants items

        :param list items: items
        :rtype list
        :return: distinct items
        """
        items_hash = defaultdict()
        for item in items:
            merchant_id = item.get('merchant_info').get('id')
            if merchant_id in items_hash:
                continue
            items_hash[merchant_id] = item
        return list(items_hash.values())
