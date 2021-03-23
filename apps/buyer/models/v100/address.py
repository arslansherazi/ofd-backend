from django.db import models
from django.db.models import Count

from apps.buyer.models.v100.buyer import Buyer


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, db_index=True)
    building = models.CharField(max_length=100, null=True, default=None)
    street = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    tag = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'buyer'
        db_table = 'address'

    @classmethod
    def save_address(cls, buyer_id, building_address, street_address, state_address, latitude, longitude, tag):
        """
        Saves address into db

        :param int buyer_id: buyer id
        :param str building_address: building address
        :param str street_address: street address
        :param str state_address: state address
        :param float latitude: latitude
        :param float longitude: longitude
        :param str tag: address tag

        :rtype int
        :returns address id
        """
        address = cls(
            buyer_id=buyer_id, building=building_address, street=street_address,
            state=state_address, latitude=latitude, longitude=longitude, tag=tag
        )
        address.save()
        return address.id

    @classmethod
    def get_addresses_count(cls, buyer_id):
        """
        Gets addresses count

        :param int buyer_id: buyer id

        :rtype int
        :returns addresses count
        """
        _q = cls.objects
        _q = _q.filter(buyer_id=buyer_id)
        addresses_data = _q.values(addresses_count=Count('id')).first()
        if addresses_data:
            return addresses_data.get('addresses_count')
        return 0

    @classmethod
    def verify_address(cls, buyer_id, building_address, street_address, state_address, tag):
        """
        Verify duplicate address

        :param int buyer_id: buyer id
        :param str building_address: building address
        :param str street_address: street address
        :param str state_address: state address
        :param str tag: address tag

        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(
            buyer_id=buyer_id, building=building_address, street=street_address, state=state_address, tag=tag
        )
        address = _q.values('id')
        if address:
            return True
        return False

    @classmethod
    def get_addresses(cls, buyer_id):
        """
        Gets all addresses

        :param int buyer_id: buyer id

        :rtype list
        :returns buyer addresses
        """
        _q = cls.objects
        _q = _q.filter(buyer_id=buyer_id)
        addresses = _q.values('id', 'building', 'street', 'state', 'latitude', 'longitude', 'tag')
        return addresses

    @classmethod
    def update_address(cls, address_id, building_address, street_address, state_address, latitude, longitude, tag):
        """
        Updates address

        :param int address_id: address id
        :param str building_address: building address
        :param str street_address: street address
        :param str state_address: state address
        :param float latitude: latitude
        :param float longitude: longitude
        :param str tag: address tag

        :rtype int
        :returns address id
        """
        address = cls.objects.get(id=address_id)
        if building_address:
            address.building = building_address
        if street_address:
            address.street = street_address
        if state_address:
            address.state = state_address
        if latitude:
            address.latitude = latitude
        if longitude:
            address.longitude = longitude
        if tag:
            address.tag = tag
        address.save()
        return address.id

    @classmethod
    def verify_buyer_address(cls, buyer_id, address_id):
        """
        Verifies that either buyer address exists or not

        :param int buyer_id: buyer id
        :param int address_id: address id

        :rtype bool
        """
        _q = cls.objects
        _q = _q.filter(id=address_id, buyer_id=buyer_id)
        address = _q.values('id').first()
        if address:
            return True
        return False

    @classmethod
    def delete_address(cls, address_id):
        """
        Deletes address

        :param int address_id: address id
        """
        address = cls.objects.get(id=address_id)
        address.delete()
