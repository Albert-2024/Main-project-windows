# Generated by Django 5.0.1 on 2024-02-06 02:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0012_deliveryregistration'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeliveryRegistration',
            new_name='DeliveryRegistrationRequest',
        ),
    ]
