from django.core.cache import cache
from django.db import models
from django.utils import timezone

from models.menu import Menu
from models.merchant import Merchant


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    unit = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.IntegerField()
    discount = models.IntegerField(null=False, default=0, db_index=True)
    image_url = models.TextField()
    rating = models.FloatField(null=True, default=None, db_index=True)
    total_rating = models.FloatField(null=True, default=None)
    rating_count = models.IntegerField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField(null=True, default=None)

    class Meta:
        app_label = 'apis'
        db_table = 'menu_item'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = timezone.now()
        else:
            self.updated_date = timezone.now()
        return super(MenuItem, self).save(*args, **kwargs)

    @classmethod
    def save_menu_item(cls, merchant_id, menu_id, name, unit, quantity, price, image_url):
        """
        Saves menu item

        :param int merchant_id: merchant id
        :param int menu_id: menu id
        :param str name: name
        :param str unit: unit
        :param int quantity: quantity
        :param int price: price
        :param str image_url: image url
        :rtype int
        :returns menu item id
        """
        menu_item = cls(
            merchant_id=merchant_id, menu_id=menu_id, name=name, unit=unit, quantity=quantity, price=price,
            image_url=image_url
        )
        menu_item.save()
        menu_item_id = menu_item.id
        return menu_item_id

    @classmethod
    def get_items_count(cls, merchant_id):
        """
        Gets no of merchant items

        :param int merchant_id: merchant id
        :rtype int
        :return: dishes count
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id)
        items_data = _q.values('id')
        if items_data:
            items_count = len(items_data)
            return items_count
        return 0

    @classmethod
    def check_duplicate_menu_item(cls, merchant_id, name):
        """
        Checks either menu item already exists or not

        :param int merchant_id: merchant id
        :param str name: menu item name
        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id, name=name)
        menu_item = _q.values()
        if menu_item:
            return True
        return False

    @classmethod
    def save_rating(cls, ratings):
        """
        Saves ratings of menu items

        :param dict ratings: ratings
        """
        menu_items_ids = list(ratings.keys())
        menu_items = []
        for menu_item_id in menu_items_ids:
            menu_item = cls.objects.get(id=menu_item_id)
            menu_item_rating = menu_item.rating
            rating = ratings.get(str(menu_item.id))
            if not menu_item_rating:
                menu_item.rating = rating
                menu_item.total_rating = rating
                menu_item.rating_count = 1
            else:
                rating_count = menu_item.rating_count + 1
                menu_item_rating = (menu_item.total_rating + rating) / rating_count
                menu_item.total_rating += rating
                menu_item.rating = menu_item_rating
                menu_item.rating_count = rating_count
            menu_items.append(menu_item)
        cls.objects.bulk_update(menu_items, ['rating', 'rating_count', 'total_rating'])

    @classmethod
    def get_menu_item(cls, menu_item_id, merchant_id=None):
        """
        Gets menu item

        :param int menu_item_id: menu item id
        :param int merchant_id: merchant id
        :rtype dict
        :return: menu item
        """
        cache_key = 'MenuItem:get_menu_item:{menu_item_id}_{merchant_id}'.format(
            menu_item_id=menu_item_id, merchant_id=merchant_id
        )
        cache_value = cache.get(cache_key)
        if cache_value:
            return cache_value
        _q = cls.objects
        if merchant_id:
            _q = _q.filter(merchant_id=merchant_id)
        _q = _q.filter(id=menu_item_id)
        menu_item = _q.values('menu_id', 'image_url').first()
        cache.set(cache_key, menu_item)
        return menu_item

    @classmethod
    def update_menu_item(
            cls, menu_item_id, name=None, unit=None, price=None, quantity=None, image_url=None,
            discount=None, is_activated=False, is_deactivated=False
    ):
        """
        Updates menu item

        :param int menu_item_id: menu item id
        :param str name: name
        :param str unit: unit
        :param int price: price
        :param int quantity: quantity
        :param str image_url: image url
        :param int discount: discount
        :param bool is_activated: menu item activation flag
        :param bool is_deactivated: menu item deactivation flag
        """
        _q = cls.objects
        menu_item = _q.filter(id=menu_item_id)
        if name:
            menu_item.update(name=name)
        if unit:
            menu_item.update(unit=unit)
        if price:
            menu_item.update(price=price)
        if quantity:
            menu_item.update(quantity=quantity)
        if image_url:
            menu_item.update(image_url=image_url)
        if discount:
            menu_item.update(discount=discount)
        if is_activated:
            menu_item.update(is_active=True)
        if is_deactivated:
            menu_item.update(is_active=False)

    @classmethod
    def delete_menu_item(cls, menu_item_id):
        """
        Deletes menu item

        :param int menu_item_id: menu item id
        """
        menu_item = cls.objects.get(id=menu_item_id)
        menu_item.delete()
