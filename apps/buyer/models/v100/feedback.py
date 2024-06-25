from django.db import models
from django.db.models import F

from apps.buyer.models.v100.buyer import Buyer
from apps.merchant.models.v100.menu_item import MenuItem


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, db_index=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    review = models.TextField(max_length=255)
    rating = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'buyer'
        db_table = 'feedback'

    @classmethod
    def save_feedback(cls, buyer_id, feedbacks):
        """
        Saves feedbacks of order items

        :param int buyer_id: buyer id
        :param dict feeedbacks: feedbacks
        """
        items_feedbacks = []
        for menu_item_id, feedback in feedbacks.items():
            item_feedback = cls(
                buyer_id=buyer_id,
                menu_item_id=int(menu_item_id),
                review=feedback.get('review'),
                rating=feedback.get('rating')
            )
            items_feedbacks.append(item_feedback)
        cls.objects.bulk_create(items_feedbacks)

    @classmethod
    def get_feedbacks(cls, item_id):
        """
        Gets feedbacks

        :param int item_id: menu_item_id
        """
        _q = cls.objects
        _q = _q.filter(menu_item_id=item_id)
        feedbacks = _q.values(
            'id', 'review', 'rating', 'created_date', reviewer_image_url=F('buyer__user__profile_image_url'),
            reviewer_username=F('buyer__user__username')
        )
        for feedback in feedbacks:
            feedback['feedback_date'] = feedback.get('created_date').strftime('%d %b, %Y')
        return feedbacks
