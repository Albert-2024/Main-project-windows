# Generated by Django 4.2.5 on 2023-10-07 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0003_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(default='', null=True),
        ),
    ]