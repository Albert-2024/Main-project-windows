# Generated by Django 4.2.5 on 2023-10-12 04:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app2', '0007_sellerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerprofile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]