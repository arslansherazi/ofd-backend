from django.db import models

from models.buyer import Buyer


class NotificationsToken(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    notifications_token = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'notifications_token'

    @classmethod
    def save_notifications_token(cls, buyer_id, notifications_token):
        """
        Saves notifications token into db

        :param int buyer_id: buyer id
        :param str notifications_token: notifications token

        :rtype bool
        """
        notifications_token = cls(buyer_id=buyer_id, notifications_token=notifications_token)
        notifications_token.save()

    @classmethod
    def verify_duplicate_token(cls, buyer_id, notifications_token):
        """
        Verifies duplicate notifications token

        :param int buyer_id: buyer id
        :param str notifications_token: notifications token

        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(buyer_id=buyer_id, notifications_token=notifications_token)
        notifications_token = _q.values('notifications_token').first()
        if notifications_token:
            return True
        return False

    @classmethod
    def get_notifications_token(cls, buyer_id):
        """
        Gets notifications token

        :param int buyer_id: buyer id

        :rtype str
        :returns notifications token
        """
        _q = cls.objects
        _q = _q.filter(buyer_id=buyer_id)
        notifications_token = _q.values('notifications_token').first()
        if notifications_token:
            return notifications_token.get('notifications_token')
        return ''
