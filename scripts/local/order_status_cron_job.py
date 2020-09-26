import os
import sys

import schedule

from wrappers.py_sql import PySQL

PACKAGE_PARENT = '../../'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


def handle_placed_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Accepted', 'Placed']
    py_sql.save_changes()


def handle_accepted_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Under Preparation', 'Accepted']
    py_sql.save_changes()


def handle_under_preparation_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['On Route', 'Under Preparation']
    py_sql.save_changes()


def handle_on_route_order_status(py_sql):
    py_sql.query = 'UPDATE order_history SET status=%s where status=%s'
    py_sql.params = ['Completed', 'On Route']
    py_sql.save_changes()


if __name__ == '__main__':
    connection = {
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'ofd_db',
        'user': 'root',
        'password': 'rootroot'
    }
    py_sql = PySQL(**connection)
    schedule.every(1).minutes.do(handle_placed_order_status, py_sql)
    schedule.every(2).minutes.do(handle_accepted_order_status, py_sql)
    schedule.every(3).minutes.do(handle_under_preparation_order_status, py_sql)
    schedule.every(5).minutes.do(handle_on_route_order_status, py_sql)

    while True:
        schedule.run_pending()
