# Generated by Django 4.2 on 2024-03-20 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0004_remove_delivery_picked_up_at_delivery_deliveryt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='delivery',
            old_name='deliveryt',
            new_name='delivery',
        ),
    ]
