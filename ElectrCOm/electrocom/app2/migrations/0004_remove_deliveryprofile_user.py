# Generated by Django 4.2.5 on 2024-02-22 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_deliveryprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryprofile',
            name='user',
        ),
    ]