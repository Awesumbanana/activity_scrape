from django.db import models
from decimal import Decimal


class ActivityDetails(models.Model):
    activity_id = models.IntegerField(default=1)
    activity_name = models.CharField(max_length=50, verbose_name='Experience Name', default='')
    activity_type = [
        ('ACT', 'Activity'),
        ('EVE', 'Event'),
        ('SCH', 'Schedule')
    ]
    activity_description = models.TextField
    activity_experience_image = models.URLField
    website = models.TextField(default='')
    commons_category = models.TextField('Commons Category', default='')
    images = models.TextField(default='')

    address_line_1 = models.TextField('Address Line 1', default='')
    address_line_2 = models.TextField('Address Line 2', default='')
    address_city = models.CharField(max_length=30, verbose_name='City', default='')
    address_state = models.CharField(max_length=30, verbose_name='State', default='')
    address_zip = models.CharField(max_length=15, default='')
    address_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitude', default=Decimal('0.00000'))
    address_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitude', default=Decimal('0.00000'))

