# Generated by Django 4.1.2 on 2022-10-11 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_car_orderhistory_car'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhistory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
