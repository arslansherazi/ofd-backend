from collections import defaultdict

from django.db import models
from django.db.models import F

from models.favourite import Favourite
from models.menu_item import MenuItem


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'ingredient'

    @classmethod
    def save_menu_item_ingredients(cls, menu_item_id, ingredients):
        """
        Saves menu item ingredients

        :param int menu_item_id: menu item id
        :param list ingredients: menu item ingredients
        """
        ingredients_objects = []
        for ingredient in ingredients:
            ingredient_object = cls(
                menu_item_id=menu_item_id,
                name=ingredient.get('name'),
                unit=ingredient.get('unit'),
                quantity=ingredient.get('quantity')
            )
            ingredients_objects.append(ingredient_object)
        cls.objects.bulk_create(ingredients_objects)

    @classmethod
    def get_menu_item_ingredients(cls, menu_item_id):
        """
        Gets menu item ingredients

        :param int menu_item_id: menu item id
        :rtype list
        :return: menu item ingredients
        """
        _q = cls.objects
        _q = _q.filter(menu_item_id=menu_item_id)
        menu_item_ingredients = _q.values('name', 'quantity', 'unit')
        return menu_item_ingredients

    @classmethod
    def get_items_data(
            cls, menu_id=None, merchant_id=None, is_menu_items=False, location_id=None, is_takeaway=False,
            is_delivery=False, is_discounted=False, is_top_rated=False, is_buyer=False, user_id=None,
            menu_items_ids=None, query=None
    ):
        """
        Gets items data

        :param int menu_id: menu id
        :param int merchant_id: merchant id
        :param bool is_menu_items: menu items flag
        :param int location_id: location id
        :param bool is_takeaway: takeaway flag
        :param bool is_delivery: delivery flag
        :param bool is_discounted: discounted items flag
        :param bool is_top_rated: top rated items flag
        :param bool is_buyer: buyer flag
        :param int user_id: user id
        :param list menu_items_ids: menu items ids
        :param str query: search query
        :rtype list
        :return: items data
        """
        _q = cls.objects
        _q = _q.select_related('menu_item', 'merchant')
        if is_menu_items:
            _q = _q.filter(menu_item__menu_id=menu_id, menu_item__merchant__id=merchant_id)
            if is_buyer:
                _q = _q.filter(menu_item__is_active=True)
        if location_id:
            _q = _q.filter(menu_item__merchant__location_id=location_id, menu_item__is_active=True)
        if is_discounted:
            _q = _q.filter(menu_item__discount__gt=0)
        if is_top_rated:
            _q = _q.filter(menu_item__rating__gt=0)
        if is_takeaway:
            _q = _q.filter(menu_item__merchant__is_takeaway_enabled=True)
        if is_delivery:
            _q = _q.filter(menu_item__merchant__is_delivery_enabled=True)
        if menu_items_ids:
            _q = _q.filter(menu_item__id__in=menu_items_ids)
        if query:
            _q = _q.filter(menu_item__name=query)
        menu_items_data = _q.values(
            'menu_item_id', ingredient_id=F('id'), ingredient_name=F('name'), ingredient_quantity=F('quantity'),
            ingredient_unit=F('unit'), menu_item_name=F('menu_item__name'),
            menu_item_price=F('menu_item__price'), menu_item_unit=F('menu_item__unit'),
            menu_item_discount=F('menu_item__discount'), menu_item_image_url=F('menu_item__image_url'),
            menu_item_rating=F('menu_item__rating'), menu_item_rating_count=F('menu_item__rating_count'),
            is_active=F('menu_item__is_active'), menu_item_quantity=F('menu_item__quantity'),
            merchant_id=F('menu_item__merchant_id'), merchant_name=F('menu_item__merchant__name'),
            merchant_latitude=F('menu_item__merchant__latitude'), merchant_longitude=F('menu_item__merchant__longitude'),
            merchant_image_url=F('menu_item__merchant__user__profile_image_url'), menu_id=F('menu_item__menu_id'),
            merchant_address=F('menu_item__merchant__address'), merchant_contact_no=F('menu_item__merchant__contact_no'),
            is_takeaway=F('menu_item__merchant__is_takeaway_enabled'),
            is_delivery=F('menu_item__merchant__is_delivery_enabled')
        )
        menu_items = {}
        menu_items_ids = []
        for menu_item_data in menu_items_data:
            menu_item_id = menu_item_data.get('menu_item_id')
            menu_items_ids.append(menu_item_id)
            menu_item_ingredient = {
                'id': menu_item_data.get('ingredient_id'),
                'name': menu_item_data.get('ingredient_name'),
                'quantity': menu_item_data.get('ingredient_quantity'),
                'unit': menu_item_data.get('ingredient_unit'),
            }
            if menu_item_id not in menu_items:
                menu_items[menu_item_id] = {
                    'id': menu_item_id,
                    'name': menu_item_data.get('menu_item_name'),
                    'price': menu_item_data.get('menu_item_price'),
                    'unit': menu_item_data.get('menu_item_unit'),
                    'quantity': menu_item_data.get('menu_item_quantity'),
                    'discount': menu_item_data.get('menu_item_discount'),
                    'image_url': menu_item_data.get('menu_item_image_url'),
                    'rating': menu_item_data.get('menu_item_rating'),
                    'rating_count': menu_item_data.get('menu_item_rating_count'),
                    'ingredients': [],
                    'is_favourite': False,
                    'merchant_info': {
                        'id': menu_item_data.get('merchant_id'),
                        'name': menu_item_data.get('merchant_name'),
                        'image_url': menu_item_data.get('merchant_image_url'),
                        'latitude': menu_item_data.get('merchant_latitude'),
                        'longitude': menu_item_data.get('merchant_longitude'),
                        'address': menu_item_data.get('merchant_address'),
                        'contact_no': menu_item_data.get('merchant_contact_no'),
                        'is_takeaway': menu_item_data.get('is_takeaway'),
                        'is_delivery': menu_item_data.get('is_delivery'),
                    },
                    'menu_id': menu_item_data.get('menu_id')
                }
            menu_items[menu_item_id]['ingredients'].append(menu_item_ingredient)
        favourites_menu_items_ids = Favourite.get_menu_item_favourite_flags(user_id, menu_items_ids)
        for menu_item_data in menu_items_data:
            menu_item_id = menu_item_data.get('menu_item_id')
            if menu_item_id in favourites_menu_items_ids:
                menu_items[menu_item_id]['is_favourite'] = True
        return list(menu_items.values())

    @classmethod
    def delete_ingredients(cls, ingredient_ids=None):
        """
        Deletes ingredients

        :param list ingredient_ids: ingredient ids
        """
        _q = cls.objects
        ingredients = _q.filter(id__in=ingredient_ids)
        ingredients.delete()

    @classmethod
    def update_ingredients(cls, updated_ingredients_data):
        """
        Updates ingredients of menu item

        :param list updated_ingredients_data: updated ingredients data
        """
        updated_ingredients = []
        for updated_ingredient_data in updated_ingredients_data:
            ingredient_id = updated_ingredient_data.get('id')
            ingredient_data = cls.objects.get(id=ingredient_id)
            ingredient_data.name = updated_ingredient_data.get('name')
            ingredient_data.quantity = updated_ingredient_data.get('quantity')
            ingredient_data.unit = updated_ingredient_data.get('unit')
            updated_ingredients.append(ingredient_data)
        cls.objects.bulk_update(updated_ingredients, ['name', 'quantity', 'unit'])

    @classmethod
    def get_menu_items_ingredients(cls, menu_items_ids):
        """
        Gets menu items ingredients

        :param list menu_items_ids: menu items ids
        :rtype list
        :return: menu items ingredients
        """
        _q = cls.objects
        _q = _q.filter(menu_item_id__in=menu_items_ids)
        ingredients_data = _q.values('id', 'menu_item_id', 'name', 'quantity', 'unit')
        menu_items_ingredients = defaultdict(list)
        for ingredient_data in ingredients_data:
            menu_item_id = ingredient_data.get('menu_item_id')
            ingredient = {
                'ingredient_id': ingredient_data.get('id'),
                'ingredient_name': ingredient_data.get('name'),
                'ingredient_unit': ingredient_data.get('unit'),
                'ingredient_quantity': ingredient_data.get('quantity')
            }
            menu_items_ingredients[menu_item_id].append(ingredient)
        return menu_items_ingredients
