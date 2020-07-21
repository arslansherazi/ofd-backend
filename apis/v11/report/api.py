from common.base_resource import BasePostResource
from models.report import Report


class ReportApi(BasePostResource):
    version = 12
    end_point = 'report'

    def initialize_class_attributes(self):
        """
        Initializes class attributes
        """
        self.merchant_id = self.current_user_info.get('merchant_id')
        self.merchant_report = {}

    def get_report_data(self):
        """
        Gets report data
        """
        self.merchant_report = Report.get_report(self.merchant_id)

    def prepare_response(self):
        """
        Prepares response
        """
        self.response = {
            'data': {
                'current_day_orders': self.merchant_report.get('current_day_orders', 0),
                'current_day_revenue': self.merchant_report.get('current_day_revenue', 0),
                'current_week_orders': self.merchant_report.get('current_week_orders', 0),
                'current_week_revenue': self.merchant_report.get('current_week_revenue', 0),
                'current_month_orders': self.merchant_report.get('current_month_orders', 0),
                'current_month_revenue': self.merchant_report.get('current_month_revenue', 0),
                'total_orders': self.merchant_report.get('total_orders', 0),
                'total_revenue': self.merchant_report.get('total_revenue', 0)
            }
        }

    def process_request(self):
        """
        Process request
        """
        self.initialize_class_attributes()
        self.get_report_data()
        self.prepare_response()
