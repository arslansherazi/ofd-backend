from django.db import models
from django.db.models import Count, F

from apis.models import User
from models.menu_item import MenuItem
from repositories.v12.buyer_repo import BuyerRepository


class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'favourite'

    @classmethod
    def insert_favourite_into_db(cls, user_id, menu_item_id):
        """
        Inserts favourite menu item into db

        :param  int user_id: user id
        :param  int menu_item_id: menu item id
        """
        favourite = cls(user_id=user_id, menu_item_id=menu_item_id)
        favourite.save()

    @classmethod
    def remove_favourite_menu_item(cls, user_id, menu_item_id):
        """
        Remove favourite menu item from db

        :param  int user_id: user id
        :param  int menu_item_id: menu item id
        """
        _q = cls.objects
        favourite = _q.filter(menu_item_id=menu_item_id, user_id=user_id)
        favourite.delete()

    @classmethod
    def get_favourites_from_db(cls, user_id):
        """
        Gets favourites from db

        :param  int user_id: user id
        :rtype list, list
        :returns favourites data, favourite menu items ids
        """
        _q = cls.objects
        _q = _q.select_related('menu_item', 'merchant')
        _q = _q.filter(user_id=user_id)
        favourites_data = _q.values(
            'menu_item_id', menu_item_name=F('menu_item__name'), menu_item_price=F('menu_item__price'),
            menu_item_unit=F('menu_item__unit'), menu_item_discount=F('menu_item__discount'),
            menu_item_image_url=F('menu_item__image_url'), menu_item_rating=F('menu_item__rating'),
            menu_item_rating_count=F('menu_item__rating_count'), is_active=F('menu_item__is_active'),
            menu_item_quantity=F('menu_item__quantity'), merchant_id=F('menu_item__merchant_id'),
            merchant_name=F('menu_item__merchant__name'),
            merchant_image_url=F('menu_item__merchant__user__profile_image_url')
        )
        menu_items_ids = []
        for favourite_data in favourites_data:
            menu_item_id = favourite_data.get('menu_item_id')
            menu_items_ids.append(menu_item_id)
        return favourites_data, menu_items_ids

    @classmethod
    def get_favourite_menu_items_ids(cls, user_id):
        """
        Gets favourite menu items ids

        :param int user_id: user id
        rtype: list
        :return: favourite menu items ids
        """
        _q = cls.objects
        _q = _q.filter(user_id=user_id)
        favourites_data = _q.values('menu_item_id')
        favourites_menu_items_ids = []
        for favourite_data in favourites_data:
            favourite_menu_item_id = favourite_data.get('menu_item_id')
            favourites_menu_items_ids.append(favourite_menu_item_id)
        return favourites_menu_items_ids

    @classmethod
    def get_favourites_count(cls, user_id):
        """
        Gets favourite count

        :param int user_id: user id
        rtype: int
        :return: favourites count
        """
        _q = cls.objects
        _q = _q.filter(user_id=user_id)
        _q = _q.values('user_id')
        favourites_count = _q.annotate(favourites_count=Count('id'))
        if favourites_count:
            return favourites_count[0].get('favourites_count')
        return BuyerRepository.NO_FAVOURITES_COUNT

    @classmethod
    def check_favourite_existance(cls, user_id, menu_item_id):
        """
        Checks either favourite exists against user or not

        :param int user_id: user id
        :param int menu_item_id: menu item id

        rtype: boolean
        """
        _q = cls.objects
        _q = _q.filter(menu_item_id=menu_item_id, user_id=user_id)
        favourite = _q.values('id')
        if favourite:
            return True
        return False

    @classmethod
    def get_menu_item_favourite_flags(cls, user_id, menu_items_ids):
        """
        Gets items favourites

        :param int user_id: user id
        :param list menu_items_ids: menu items ids
        :return: items favourite flags
        """
        _q = cls.objects
        _q = _q.filter(user_id=user_id, menu_item_id__in=menu_items_ids)
        favourite_menu_items_ids_data = _q.values('menu_item_id')
        favourite_menu_items_ids = []
        for favourite_menu_items_id_data in favourite_menu_items_ids_data:
            favourite_menu_item_id = favourite_menu_items_id_data.get('menu_item_id')
            favourite_menu_items_ids.append(favourite_menu_item_id)
        return favourite_menu_items_ids

    @classmethod
    def verify_favourite(cls, user_id, menu_item_id):
        """
        Verifies that either menu item is marked as favourite against particular user or not

        :param int user_id: user id
        :param int menu_item_id: menu item id
        :rtype bool
        """
        _q = cls.objects
        favourite = _q.filter(user_id=user_id, menu_item_id=menu_item_id)
        if favourite:
            return True
        return False
