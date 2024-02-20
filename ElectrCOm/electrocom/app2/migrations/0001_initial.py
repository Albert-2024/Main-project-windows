# Generated by Django 4.2.5 on 2024-02-19 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Customer'), (2, 'Seller'), (3, 'Delivery')], default=1, null=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superadmin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('product_name', models.CharField(max_length=255, null=True)),
                ('brand_name', models.CharField(max_length=255, null=True)),
                ('price', models.CharField(max_length=255, null=True)),
                ('image1', models.ImageField(blank=True, max_length=255, null=True, upload_to='sample/')),
                ('image2', models.ImageField(blank=True, max_length=255, null=True, upload_to='sample/')),
                ('image3', models.ImageField(blank=True, max_length=255, null=True, upload_to='sample/')),
                ('description', models.TextField(max_length=255, null=True)),
                ('category', models.CharField(max_length=255, null=True)),
                ('stock', models.PositiveIntegerField(default=0, max_length=255)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sellerRegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gst', models.TextField(max_length=30)),
                ('pan', models.TextField(max_length=30)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('feedback', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gst', models.TextField(max_length=30)),
                ('pan', models.TextField(max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(default='', null=True)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpeaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery', models.CharField(max_length=255, null=True)),
                ('s_connectivity', models.CharField(max_length=255, null=True)),
                ('s_type', models.CharField(max_length=255, null=True)),
                ('special_features', models.CharField(max_length=255, null=True)),
                ('weight', models.CharField(max_length=255, null=True)),
                ('charging', models.CharField(max_length=255, null=True)),
                ('working', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductMobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wireless', models.CharField(max_length=255, null=True)),
                ('m_os', models.CharField(max_length=255, null=True)),
                ('cellular', models.CharField(max_length=255, null=True)),
                ('memory', models.CharField(max_length=255, null=True)),
                ('connectivity', models.CharField(max_length=255, null=True)),
                ('m_screen', models.CharField(max_length=255, null=True)),
                ('wireless_network_technology', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=255, null=True)),
                ('ram', models.TextField(max_length=255, null=True)),
                ('processor', models.CharField(max_length=255, null=True)),
                ('camrear', models.CharField(max_length=255, null=True)),
                ('camfront', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductLap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screen_size', models.CharField(max_length=255, null=True)),
                ('space', models.CharField(max_length=255, null=True)),
                ('ram', models.CharField(max_length=255, null=True)),
                ('os', models.CharField(max_length=255, null=True)),
                ('graphics', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=255, null=True)),
                ('processor', models.CharField(max_length=255, null=True)),
                ('storage', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductHeadset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery', models.CharField(max_length=255, null=True)),
                ('color', models.CharField(max_length=255, null=True)),
                ('form_factor', models.CharField(max_length=255, null=True)),
                ('h_connectivity', models.CharField(max_length=255, null=True)),
                ('weight', models.CharField(max_length=255, null=True)),
                ('charging', models.CharField(max_length=255, null=True)),
                ('working', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(max_length=3)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('items', models.ManyToManyField(to='app2.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='DeliveryRegistrationRequests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING', max_length=10)),
                ('lic_num', models.CharField(max_length=15)),
                ('rc_num', models.CharField(max_length=30)),
                ('pan', models.CharField(max_length=30)),
                ('aadhar_num', models.CharField(max_length=40)),
                ('feedback', models.TextField(blank=True)),
                ('is_registered', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=70)),
                ('country', models.CharField(max_length=70)),
                ('state', models.CharField(max_length=70)),
                ('district', models.CharField(max_length=70)),
                ('pincode', models.CharField(max_length=70)),
                ('bank', models.CharField(max_length=70)),
                ('acc_num', models.CharField(max_length=70)),
                ('ifsc', models.CharField(max_length=70)),
                ('delivery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.deliveryregistrationrequests')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cartstock', models.PositiveIntegerField(default=1)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField(default=0)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app2.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('authors', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
