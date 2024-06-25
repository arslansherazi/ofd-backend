from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat

from apps.buyer.models.v100.order import Order


class Driver(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'merchant'
        db_table = 'driver'

    @classmethod
    def add_driver(cls, order_id, first_name, last_name, vehicle_model, vehicle_number, contact_no):
        """
        Adds driver into db

        :param int order_id: order id
        :param str first_name: first name
        :param str last_name: last name
        :param str vehicle_model: vehicle model
        :param str vehicle_number: vehicle number
        :param int contact_no: contact no
        """
        driver = cls(
            order_id=order_id, first_name=first_name, last_name=last_name, vehicle_model=vehicle_model,
            vehicle_number=vehicle_number, contact_no=contact_no
        )
        driver.save()

    @classmethod
    def get_driver_info(cls, order_id):
        """
        Gets driver info of order

        :param int order_id: order id
        :returns driver info
        :rtype dict
        """
        _q = cls.objects
        _q = _q.filter(order_id=order_id)
        driver_info = _q.values(
            'vehicle_model', 'vehicle_number', 'contact_no', name=Concat('first_name', Value(' '), 'last_name')
        ).first()
        return driver_info
