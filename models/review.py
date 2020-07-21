from django.db import models

from models.buyer import Buyer
from models.menu_item import MenuItem


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, db_index=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    review = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'review'

    @classmethod
    def save_review(cls, buyer_id, reviews):
        """
        Saves reviews of order items

        :param int buyer_id: buyer id
        :param dict reviews: reviews
        """
        items_reviews = []
        for menu_item_id, review in reviews.items():
            item_review = cls(
                buyer_id=buyer_id,
                menu_item_id=menu_item_id,
                review=review
            )
            items_reviews.append(item_review)
        cls.objects.bulk_create(items_reviews)
