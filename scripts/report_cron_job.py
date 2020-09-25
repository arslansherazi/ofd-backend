import os
import sys
from datetime import date

import schedule
from django.conf import settings

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from wrappers.py_sql import PySQL


def reset_last_day_report(py_sql):
    py_sql.query = 'UPDATE report SET current_day_orders = 0, current_day_revenue = 0'
    py_sql.save_changes()


def reset_last_week_report():
    py_sql.query = 'UPDATE report SET current_week_orders = 0, current_week_revenue = 0'
    py_sql.save_changes()


def reset_last_month_report():
    if date.today().day == 1:
        py_sql.query = 'UPDATE report SET current_month_orders = 0, current_month_revenue = 0'
        py_sql.save_changes()


if __name__ == '__main__':
    connection = {
        'host': settings.DATABASES.get('default').get('HOST'),
        'port': 3306,
        'database': settings.DATABASES.get('default').get('NAME'),
        'user': settings.DATABASES.get('default').get('USER'),
        'password': settings.DATABASES.get('default').get('PASSWORD')
    }
    py_sql = PySQL(**connection)
    schedule.every().day.at('00:00').do(reset_last_day_report, py_sql)
    schedule.every().monday.at('00:00').do(reset_last_week_report, py_sql)
    schedule.every().day.at('00:00').do(reset_last_month_report(), py_sql)

    while True:
        schedule.run_pending()
