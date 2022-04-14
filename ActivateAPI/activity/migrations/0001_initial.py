# Generated by Django 4.0.3 on 2022-04-08 08:23

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_id', models.IntegerField(default=1)),
                ('activity_name', models.CharField(default='', max_length=50, verbose_name='Experience Name')),
                ('address_line_1', models.TextField(default='', verbose_name='Address Line 1')),
                ('address_line_2', models.TextField(default='', verbose_name='Address Line 2')),
                ('address_city', models.CharField(default='', max_length=30, verbose_name='City')),
                ('address_state', models.CharField(default='', max_length=30, verbose_name='State')),
                ('address_zip', models.CharField(default='', max_length=15)),
                ('address_latitude', models.DecimalField(decimal_places=9, default=Decimal('0.0000'), max_digits=9, verbose_name='Latitude')),
                ('address_longitude', models.DecimalField(decimal_places=9, default=Decimal('0.0000'), max_digits=9, verbose_name='Longitude')),
            ],
        ),
    ]