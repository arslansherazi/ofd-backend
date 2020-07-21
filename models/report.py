from django.db import models

from models.merchant import Merchant


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, db_index=True)
    current_day_orders = models.IntegerField(default=0)
    current_day_revenue = models.IntegerField(default=0)
    current_week_orders = models.IntegerField(default=0)
    current_week_revenue = models.IntegerField(default=0)
    current_month_orders = models.IntegerField(default=0)
    current_month_revenue = models.IntegerField(default=0)
    total_orders = models.IntegerField(default=0)
    total_revenue = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'report'

    @classmethod
    def update_report(cls, merchant_id, revenue):
        """
        Updates report

        :param int merchant_id: merchant id
        :param int revenue: revenue
        """
        try:
            report = cls.objects.get(merchant_id=merchant_id)
            report.current_day_orders = report.current_day_orders + 1
            report.current_day_revenue = report.current_day_revenue + revenue
            report.current_week_orders = report.current_week_orders + 1
            report.current_week_revenue = report.current_week_revenue + revenue
            report.current_month_orders = report.current_month_orders + 1
            report.current_month_revenue = report.current_month_revenue + revenue
            report.total_orders = report.total_orders + 1
            report.total_revenue = report.total_revenue + revenue
            report.save()
        except Exception:
            report = cls(
                merchant_id=merchant_id, current_day_orders=1, current_day_revenue=revenue, current_week_orders=1,
                current_week_revenue=revenue, current_month_orders=1, current_month_revenue=revenue, total_orders=1,
                total_revenue=revenue
            )
            report.save()

    @classmethod
    def get_report(cls, merchant_id):
        """
        Gets report data

        :param int merchant_id: merchant id
        :rtype dict
        :return: merchant report
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id)
        report = _q.values(
            'current_day_orders', 'current_day_revenue', 'current_week_orders', 'current_week_revenue',
            'current_month_orders', 'current_month_revenue', 'total_orders', 'total_revenue'
        ).first()
        return report
