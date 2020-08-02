from django.db import models
from django.db.models import F, Q, Value
from django.db.models.functions import Concat

from apis.models import User
from common.constants import BUYER_USER_TYPE


class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'buyer'

    @classmethod
    def insert_buyer_into_db(cls, user_id, first_name, last_name):
        """
        Inserts buyer into db

        :param  int user_id: user id
        :param str first_name: first name
        :param str last_name: last name
        :rtype int
        :returns buyer id
        """
        buyer = cls(user_id=user_id, first_name=first_name, last_name=last_name)
        buyer.save()
        buyer_id = buyer.id
        return buyer_id

    @classmethod
    def get_buyer_id(cls, user_id):
        """
        Gets buyer id

        :param int user_id: user id
        :rtype int
        :return: buyer id
        """
        _q = cls.objects
        _q = _q.filter(user_id=user_id)
        buyer_info = _q.values('id').first()
        return buyer_info.get('id', 0)

    @classmethod
    def update_data(cls, buyer_id, first_name, last_name):
        """
        Updates first name or last name

        :param int buyer_id: buyer id
        :param str first_name: first name
        :param str last_name: last name
        """
        _q = cls.objects
        buyer = _q.filter(id=buyer_id)
        if first_name:
            buyer.update(first_name=first_name)
        if last_name:
            buyer.update(last_name=last_name)

    @classmethod
    def get_buyer_login_info(cls, username=None, user_type=BUYER_USER_TYPE):
        """
        Gets buyer login info

        :param str username: username
        :param int user_type: user type
        :return buyer login info
        :rtype: dict
        """
        _q = cls.objects
        _q = _q.select_related('user')
        _q = _q.filter((Q(user__username=username) | Q(user__email=username)), user__user_type=user_type)
        buyer = _q.values(
            'user_id', 'first_name', 'last_name', username=F('user__username'), name=Concat('first_name', Value(' '), 'last_name'),  # noqa: 501
            email=F('user__email'), password=F('user__password'), is_email_verified=F('user__is_email_verified'),
            profile_image_url=F('user__profile_image_url')
        ).first()
        return buyer

    @classmethod
    def get_profile(cls, buyer_id):
        """
        Gets buyer profile

        :param int buyer_id: buyer id

        :rtype dict
        :return: buyer profile
        """
        _q = cls.objects
        _q = _q.select_related('user')
        _q = _q.filter(id=buyer_id)
        buyer_profile = _q.values(
            'first_name', 'last_name', username=F('user__email'), email=F('user__email'),
            profile_image_url=F('user__profile_image_url')
        ).first()
        return buyer_profile
