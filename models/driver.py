from django.db import models

from models.order import Order


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
        app_label = 'apis'
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
