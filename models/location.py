from django.db import models


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, db_index=True)
    boundry = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'apis'
        db_table = 'location'

    @classmethod
    def get_locations_boundries(cls):
        """
        Gets boundry of all locations
        """
        _q = cls.objects
        boundries = _q.values('id', 'boundry')
        return boundries
