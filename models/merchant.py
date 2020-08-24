from django.db import models
from django.db.models import F, Q

from apis.models import User
from common.constants import MERCHANT_USER_TYPE
from models.location import Location


class Merchant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=255, null=True)
    contact_no = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    menus_limit = models.IntegerField()
    items_limit = models.IntegerField()
    is_takeaway_enabled = models.BooleanField(db_index=True)
    is_delivery_enabled = models.BooleanField(db_index=True)
    opening_time = models.TimeField(null=True, default=None)
    closing_time = models.TimeField(null=True, default=None)
    opening_days = models.CharField(max_length=255, null=True)
    is_open_all_day = models.BooleanField(default=False)
    is_open_all_week = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'merchant'

    @classmethod
    def insert_merchant_into_db(
            cls, user_id, name, title, contact_no, address, latitude, longitude, location_id, menus_limit, items_limit,
            is_takeaway_enabled, is_delivery_enabled, opening_time, closing_time, opening_days, is_open_all_day,
            is_open_all_week
    ):
        """
        Inserts merchant into db

        :param int user_id: user id
        :param str name: name
        :param str title: title
        :param int contact_no: contact no
        :param str address: address
        :param float latitude: latitude
        :param float longitude: longitude
        :param int location_id: location id
        :param int menus_limit: menus limit
        :param int items_limit: menus items limit
        :param bool is_takeaway_enabled: takeaway flag
        :param bool is_delivery_enabled: delivery flag
        :param DateTime opening_time: opening time
        :param DateTime closing_time: closing time
        :param str opening_days: opening days
        :param bool is_open_all_day: open all day flag
        :param bool is_open_all_week: open all week flag
        :rtype int
        :returns merchant id
        """
        merchant = cls(
            user_id=user_id, name=name, title=title, contact_no=contact_no, address=address, latitude=latitude,
            longitude=longitude, menus_limit=menus_limit, items_limit=items_limit, location_id=location_id,
            is_takeaway_enabled=is_takeaway_enabled, is_delivery_enabled=is_delivery_enabled, opening_time=opening_time,
            closing_time=closing_time, opening_days=opening_days, is_open_all_day=is_open_all_day,
            is_open_all_week=is_open_all_week
        )
        merchant.save()
        merchant_id = merchant.id
        return merchant_id

    @classmethod
    def get_merchant_id(cls, user_id):
        """
        Gets merchant id

        :param int user_id: user id
        :rtype int
        :return: merchant id
        """
        _q = cls.objects
        _q = _q.filter(user_id=user_id)
        merchant_data = _q.values('id')
        merchant_id = None
        if merchant_data:
            merchant_id = merchant_data[0].get('id')
        return merchant_id

    @classmethod
    def get_menus_limit(cls, merchant_id):
        """
        Gets menus limit

        :param int merchant_id: merchant id
        :return: menus limit
        :rtype int
        """
        _q = cls.objects
        _q = _q.filter(id=merchant_id)
        merchant_data = _q.values('menus_limit')
        menus_limit = None
        if merchant_data:
            menus_limit = merchant_data[0].get('menus_limit')
        return menus_limit

    @classmethod
    def get_items_limit(cls, merchant_id):
        """
        Gets items limit

        :param int merchant_id: merchant id
        :return: items limit
        :rtype int
        """
        _q = cls.objects
        _q = _q.filter(id=merchant_id)
        merchant_data = _q.values('items_limit')
        items_limit = None
        if merchant_data:
            items_limit = merchant_data[0].get('items_limit')
        return items_limit

    @classmethod
    def update_data(
            cls, merchant_id, name, title, contact_no, address, latitude, longitude, is_delivery_enabled,
            is_takeaway_enabled
    ):
        """
        Updates data

        :param int merchant_id: merchant id
        :param str name: name
        :param str title: title
        :param int contact_no: contact no
        :param str address: address
        :param float latitude: latitude
        :param float longitude: longitude
        :param bool is_delivery_enabled: is delivery enabled flag
        :param bool is_takeaway_enabled: is takeaway enabled
        """
        _q = cls.objects
        merchant = _q.filter(id=merchant_id)
        if name:
            merchant.update(name=name)
        if title:
            merchant.update(title=title)
        if contact_no:
            merchant.update(contact_no=contact_no)
        if address:
            merchant.update(address=address)
        if latitude:
            merchant.update(latitude=latitude)
        if longitude:
            merchant.update(longitude=longitude)
        if is_delivery_enabled:
            merchant.update(is_delivery_enabled=is_delivery_enabled)
        if is_takeaway_enabled:
            merchant.update(is_takeaway_enabled=is_takeaway_enabled)

    @classmethod
    def get_merchant_availability(cls, merchant_id):
        """
        Gets merchant availability

        :param int merchant_id: merchant id
        """
        _q = cls.objects
        _q = _q.filter(id=merchant_id)
        merchant_availability = _q.values(
            'name', 'opening_time', 'closing_time', 'opening_days', 'is_open_all_day', 'is_open_all_week'
        ).first()
        return merchant_availability

    @classmethod
    def update_merchant_availability(
            cls, merchant_id, opening_time=None, closing_time=None, opening_days=None, is_open_all_day=None,
            is_open_all_week=None
    ):
        """
        Updates merchant availability

        :param int merchant_id: merchant id
        :param DateTime opening_time: opening time
        :param DateTime closing_time: closing time
        :param str opening_days: opening days
        :param bool is_open_all_day: open all day flag
        :param bool is_open_all_week: open all week flag
        """
        _q = cls.objects
        merchant = _q.filter(id=merchant_id)
        if opening_time:
            merchant.update(opening_time=opening_time)
        if closing_time:
            merchant.update(closing_time=closing_time)
        if opening_days:
            merchant.update(opening_days=opening_days)
        if is_open_all_day:
            merchant.update(is_open_all_day=is_open_all_day)
        if is_open_all_week:
            merchant.update(is_open_all_week=is_open_all_week)

    @classmethod
    def verify_merchant_existance(cls, merchant_id):
        """
        Verifies that either merchant exists or not
        :param int merchant_id: merchant id
        :rtype bool
        """
        _q = cls.objects
        merchant = _q.filter(id=merchant_id)
        if merchant:
            return True
        return False

    @classmethod
    def get_merchants_data(cls, location_id, is_delivery, is_takeaway):
        """
        Gets merchants data

        :param int location_id: location id
        :param bool is_delivery: delivery flag
        :param bool is_takeaway: takeaway flag
        :rtype list
        :returns: merchants data
        """
        _q = cls.objects
        _q = _q.filter(location_id=location_id)
        if is_takeaway:
            _q = _q.filter(is_takeaway_enabled=True)
        if is_delivery:
            _q = _q.filter(is_delivery_enabled=True)
        merchants_data = _q.values('id', 'latitude', 'longitude', 'name')
        merchants = []
        for merchant_data in merchants_data:
            merchant = {
                'id': merchant_data.get('id'),
                'coordinate': {
                    'latitude': merchant_data.get('latitude'),
                    'longitude': merchant_data.get('longitude')
                },
                'title': merchant_data.get('name')
            }
            merchants.append(merchant)
        return merchants

    @classmethod
    def get_merchant_login_info(cls, username=None, user_type=MERCHANT_USER_TYPE):
        """
        Gets merchant login info

        :param str username: username
        :param int user_type: user type
        :return merchant login info
        :rtype: dict
        """
        _q = cls.objects
        _q = _q.select_related('user')
        _q = _q.filter((Q(user__username=username) | Q(user__email=username)), user__user_type=user_type)
        merchant = _q.values(
            'name', username=F('user__username'), email=F('user__email'), password=F('user__password'),
            is_email_verified=F('user__is_email_verified'), profile_image_url=F('user__profile_image_url')
        ).first()
        return merchant

    @classmethod
    def get_profile(cls, merchant_id):
        """
        Gets merchant profile

        :param int merchant_id: merchant id

        :rtype dict
        :return: merchant profile
        """
        _q = cls.obejcts
        _q = _q.select_related('user')
        _q = _q.filter(id=merchant_id)
        merchant_profile = _q.values(
            'name', 'title', username=F('user__email'), email=F('user__email'),
            profile_image_url=F('user__profile_image_url')
        ).first()
        return merchant_profile
