import os
import sys

import geopy.distance
import schedule
from exponent_server_sdk import PushClient, PushMessage, PushServerError

from common.constants import AVERAGE_PREPARATION_TIME, BUFFER_TIME
from wrappers.py_sql import PySQL

PACKAGE_PARENT = '../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def send_notifications(status, py_sql, orders_ids=None, is_completed=False):
    if is_completed:
        py_sql.query = '''SELECT oh.id AS order_id, nt.notifications_token, m.name AS merchant_name
        FROM order_history oh 
        INNER JOIN notifications_token nt ON nt.buyer_id = oh.buyer_id
        INNER JOIN merchant m ON m.id = oh.merchant_id
        WHERE oh.status = %s
        AND oh.id = %s
        '''
        notifications_data = []
        for order_id in orders_ids:
            py_sql.params = [status, order_id]
            notification_data = py_sql.fetch_one()
            notifications_data.append(notification_data)
    else:
        py_sql.query = '''SELECT oh.id AS order_id, nt.notifications_token, m.name AS merchant_name
        FROM order_history oh 
        INNER JOIN notifications_token nt ON nt.buyer_id = oh.buyer_id
        INNER JOIN merchant m ON m.id = oh.merchant_id
        WHERE oh.status = %s
        '''
        py_sql.params = [status]
        notifications_data = py_sql.fetch_all()
    for notification_data in notifications_data:
        order_id = notification_data.get('order_id')
        notifications_token = notification_data.get('notifications_token')
        order_data = get_order_data(order_id, py_sql)
        merchant_name = notification_data.get('merchant_name')
        notification_body = 'You order from {merchant_name} is {status}'.format(
            merchant_name=merchant_name, status=status
        )
        try:
            PushClient().publish(PushMessage(to=notifications_token, body=notification_body, data=order_data))
        except PushServerError:
            pass


def get_orders_ids(status, py_sql):
    py_sql.query = 'SELECT id from order_history WHERE status=%s'
    py_sql.params = [status]
    orders_data = py_sql.fetch_all()
    orders_ids = []
    for order_data in orders_data:
        order_id = order_data.get('id')
        orders_ids.append(order_id)
    return orders_ids


def get_order_data(order_id, py_sql):
    py_sql.query = '''SELECT od.id, od.order_id, oh.order_number, oh.is_delivery, oh.delivery_address, 
    m.name AS merchant_name, m.address AS merchant_address, od.item_id AS order_item_id, mi.name AS order_item_name,
    od.item_price AS order_item_price, od.item_discount AS order_item_discount, oh.price AS order_price, 
    oh.created_date AS order_date, m.id AS merchant_id, oh.is_reviewed, m.latitude AS merchant_latitude,
    m.longitude AS merchant_longitude, oh.latitude, oh.longitude, od.item_quantity AS order_item_quantity, oh.status
    FROM order_details od
    INNER JOIN order_history oh ON od.order_id = oh.id
    INNER JOIN merchant m ON oh.merchant_id = m.id
    INNER JOIN menu_item mi ON od.item_id = mi.id
    WHERE oh.id = %s
    '''
    py_sql.params = [order_id]
    order_data = py_sql.fetch_all()
    order_final_data = {}
    for order in order_data:
        order_id = order.get('order_id')
        if order_id in order_final_data:
            order_item = {
                'id': order.get('id'),
                'item_id': order.get('order_item_id'),
                'item_name': order.get('order_item_name'),
                'item_quantity': order.get('order_item_quantity'),
                'price': order.get('order_item_price'),
                'discount': order.get('order_item_discount')
            }
            order_final_data[order_id]['order_items'].append(order_item)
        else:
            order_final_data[order_id] = {
                'id': order_id,
                'status': order.get('status'),
                'order_number': order.get('order_number'),
                'price': order.get('order_price'),
                'is_delivery': bool(order.get('is_delivery')),
                'delivery_address': order.get('delivery_address'),
                'merchant_name': order.get('merchant_name'),
                'merchant_address': order.get('merchant_address'),
                'merchant_id': order.get('merchant_id'),
                'date': order.get('order_date').strftime('%m/%d/%Y, %H:%M:%S'),
                'is_reviewed': order.get('is_reviewed'),
                'order_items': [{
                    'id': order.get('id'),
                    'item_id': order.get('order_item_id'),
                    'item_name': order.get('order_item_name'),
                    'item_quantity': order.get('order_item_quantity'),
                    'price': order.get('order_item_price'),
                    'discount': order.get('order_item_discount')
                }]
            }
            if (
                    order.get('is_delivery', False) and
                    order.get('status').lower() not in ['cancelled', 'completed']
            ):
                order_final_data[order_id]['average_delivery_time'] = calculate_delivery_time_and_distance(
                    latitude=order.get('latitude'), longitude=order.get('longitude'),
                    merchant_latitude=order.get('merchant_latitude'),
                    merchant_longitude=order.get('merchant_longitude'),
                    is_delivery=True
                )
    return order_final_data.get(order_id)


def calculate_delivery_time_and_distance(latitude, longitude, merchant_latitude, merchant_longitude, is_delivery=False):
    merchant_location = (merchant_latitude, merchant_longitude)
    buyer_location = (latitude, longitude)
    distance = geopy.distance.vincenty(merchant_location, buyer_location).km
    if is_delivery:
        delivery_time = round(distance + AVERAGE_PREPARATION_TIME + BUFFER_TIME)
        if delivery_time <= 60:
            delivery_time_with_unit = '{} MIN'.format(delivery_time)
        else:
            delivery_time_hours = delivery_time // 60
            delivery_time_minutes = delivery_time % 60
            delivery_time_with_unit = '{hours} HRS {minutes} MIN'.format(
                hours=delivery_time_hours, minutes=delivery_time_minutes
            )
        return delivery_time_with_unit
    else:
        distance_unit = 'km'
        if not distance >= 1:
            distance = distance * 1000
            distance_unit = 'm'
        distance = round(distance, 2)
        distance_with_unit = '{distance} {unit}'.format(
            distance=distance, unit=distance_unit
        )
        return distance_with_unit


def handle_placed_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Accepted', 'Placed']
    py_sql.save_changes()
    send_notifications('Accepted', py_sql)


def handle_accepted_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Under Preparation', 'Accepted']
    py_sql.save_changes()
    send_notifications('Under Preparation', py_sql)


def handle_under_preparation_order_status(py_sql):
    orders_ids = get_orders_ids('Under Preparation', py_sql)
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['On Route', 'Under Preparation']
    py_sql.save_changes()
    add_driver_information(orders_ids, py_sql)
    send_notifications('On Route', py_sql)


def handle_on_route_order_status(py_sql):
    orders_ids = get_orders_ids('On Route', py_sql)
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Completed', 'On Route']
    py_sql.save_changes()
    send_notifications('Completed', py_sql, orders_ids, is_completed=True)


def add_driver_information(orders_ids, py_sql):
    for order_id in orders_ids:
        py_sql.query = '''INSERT INTO driver 
        VALUES(first_name, last_name, vehicle_model, vehicle_number, contact_no, created_date, updated_date, order_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        py_sql.params = ['Arslan', 'Sherazi', 'United CD-70', 'LEP-5122', '03336664142', order_id]
        py_sql.save_changes()


if __name__ == '__main__':
    connection = {
        'host': 'onlinefooddepot.mysql.pythonanywhere-services.com',
        'port': 3306,
        'database': 'onlinefooddepot$ofd_db_prod',
        'user': 'onlinefooddepot',
        'password': 'ed9389d6-3157-4755-984f'
    }
    py_sql = PySQL(**connection)
    schedule.every(1).minutes.do(handle_placed_order_status, py_sql)
    schedule.every(2).minutes.do(handle_accepted_order_status, py_sql)
    schedule.every(3).minutes.do(handle_under_preparation_order_status, py_sql)
    schedule.every(5).minutes.do(handle_on_route_order_status, py_sql)

    while True:
        schedule.run_pending()
