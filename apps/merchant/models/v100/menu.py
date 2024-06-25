from django.db import models

from apps.merchant.models.v100.merchant import Merchant


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    image_url = models.TextField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'merchant'
        db_table = 'menu'

    @classmethod
    def check_duplicate_menu(cls, merchant_id, name):
        """
        Checks either menu already exists or not

        :param int merchant_id: merchant id
        :param str name: menu name
        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id, name=name)
        menu = _q.values('id')
        if menu:
            return True
        return False

    @classmethod
    def get_menus_count(cls, merchant_id):
        """
        Gets menus count of merchant

        :param int merchant_id: merchant id
        :return: menus count
        :rtype int
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id)
        menus = _q.values('id')
        return len(menus)

    @classmethod
    def add_new_menu(cls, merchant_id, name, image_url=None, is_active=True):
        """
        Adds new menu

        :param int merchant_id: merchant id
        :param str name: name
        :param str image_url: image_url
        :param bool is_active: menu activation status
        """
        menu = cls(merchant_id=merchant_id, name=name, is_active=is_active)
        if image_url:
            menu.image_url = image_url
        menu.save()

    @classmethod
    def get_menus(cls, merchant_id):
        """
        Gets menus

        :param int merchant_id: merchant id
        :rtype list
        :return: menus
        """
        _q = cls.objects
        _q = _q.filter(merchant_id=merchant_id)
        menus = _q.values('id', 'name', 'is_active', 'image_url')
        if menus:
            return menus
        return []

    @classmethod
    def update_menu(cls, menu_id, merchant_id, name, image_url, is_activate, is_deactivate):
        """
        Updates menu details. It also verifies that either menu exists against the merchant or not

        :param int menu_id: menu id
        :param int merchant_id: merchant_id
        :param str name: name
        :param str image_url: image url
        :param bool is_activate: menu activation flag
        :param bool is_deactivate: menu deactivation flag
        :return: bool
        """
        _q = cls.objects
        menu = _q.filter(id=menu_id, merchant_id=merchant_id)
        if menu:
            if name:
                menu.update(name=name)
            if image_url:
                menu.update(image_url=image_url)
            if is_activate:
                menu.update(is_active=True)
            elif is_deactivate:
                menu.update(is_active=False)
            return True
        return False

    @classmethod
    def verify_menu(cls, menu_id, merchant_id):
        """
        Verifies that either a menu exists against a merchant or not

        :param int menu_id: menu id
        :param int merchant_id: merchant_id
        :rtype bool
        """
        _q = cls.objects
        menu = _q.filter(id=menu_id, merchant_id=merchant_id)
        if menu:
            return True
        return False

    @classmethod
    def delete_menu(cls, menu_id):
        """
        Deletes menu

        :param int menu_id: menu id
        """
        menu = cls.objects.get(id=menu_id)
        menu.delete()

    @classmethod
    def get_menu_image_url(cls, menu_id):
        """
        Gets menu image url

        :param int menu_id: menu id
        :return: menu image url
        :rtype str
        """
        _q = cls.objects
        _q = _q.filter(id=menu_id)
        menu_data = _q.values('image_url').first()
        return menu_data.get('image_url', '')
