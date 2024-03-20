from time import timezone
from urllib import request
from django.conf import settings
from django.db import models
from django.db import migrations

# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.shortcuts import redirect, render

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name,last_name, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name = first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name,last_name, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    CUSTOMER = 1
    SELLER = 2
    DELIVERY = 3

    ROLE_CHOICE = (
        (CUSTOMER, 'Customer'),
        (SELLER, 'Seller'),
        (DELIVERY, 'Delivery'),
    )

    username=None
    USERNAME_FIELD = 'first_name'
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True) 
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, default=1 ,blank=True, null=True)

    # date_joined = models.DateTimeField(auto_now_add=True)
    # last_login = models.DateTimeField(auto_now_add=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    # modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)


    
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email  

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    address = models.TextField(default="", null=True)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.email

class sellerRegistrationRequest(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    gst = models.TextField(max_length=30)
    pan = models.TextField(max_length=30)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='PENDING')
    feedback = models.TextField(blank=True)
    
    def __str__(self):
        return f'Seller Registration Request: {self.user.email}'
    
    
class DeliveryRegistrationRequests(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status =  models.CharField(max_length=10,choices=[('PENDING','Pending'),('APPROVED','Approved'),('REJECTED','Rejected')],default='PENDING')
    lic_num = models.CharField(max_length=30,blank=False)
    rc_num = models.CharField(max_length=30)
    pan = models.CharField(max_length=30)
    aadhar_num=models.CharField(max_length=40)
    feedback = models.TextField(blank=True)
    is_registered = models.BooleanField(default=False)
    

    def __str__(self):
        return f'Delivery Agent Request: {self.user.email}'
    
class SellerProfile(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True)
    gst = models.TextField(max_length=30)
    pan = models.TextField(max_length=30)
    
    def __str__(self):
        return self.user.email
    

    
class Product(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    product_name = models.CharField(max_length=255, null=True)
    brand_name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    image1 = models.ImageField(upload_to='sample/', null=True, blank=True, max_length=255)
    image2 = models.ImageField(upload_to='sample/', null=True, blank=True, max_length=255)
    image3 = models.ImageField(upload_to='sample/', null=True, blank=True, max_length=255)
    description = models.TextField(max_length=1000, null=True)
    category = models.CharField(max_length=255, null=True)
    stock = models.PositiveIntegerField(max_length=255, default=0)
    
     
    def __str__(self):
        return self.product_name
    
class ProductLap(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    screen_size = models.CharField(max_length=255, null=True)
    space = models.CharField(max_length=255, null=True)
    ram = models.CharField(max_length=255, null=True)
    os = models.CharField(max_length=255, null=True)
    graphics = models.CharField(max_length=255, null=True)
    color= models.CharField(max_length=255,null=True)
    processor = models.CharField(max_length=255, null=True)
    storage = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.product.product_name
    
    
class ProductMobile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    wireless = models.CharField(max_length=255, null=True)
    m_os = models.CharField(max_length=255, null=True)
    cellular = models.CharField(max_length=255, null=True)
    memory = models.CharField(max_length=255, null=True)
    connectivity = models.CharField(max_length=255, null=True)
    m_screen = models.CharField(max_length=255, null=True)
    wireless_network_technology = models.CharField(max_length=255, null=True)
    color= models.CharField(max_length=255,null=True)
    ram = models.TextField(max_length=255, null=True)
    processor = models.CharField(max_length=255, null=True)
    camrear = models.CharField(max_length=255, null=True)
    camfront = models.CharField(max_length=255, null=True)  
    
    def __str__(self):
        return self.product.product_name

    
class ProductHeadset(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    battery = models.CharField(max_length=255, null=True)
    color= models.CharField(max_length=255,null=True)
    form_factor = models.CharField(max_length=255, null=True) 
    h_connectivity = models.CharField(max_length=255, null=True) 
    weight = models.CharField(max_length=255, null=True)
    charging = models.CharField(max_length=255, null=True) 
    working = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.product.product_name
    
class DeliveryProfile(models.Model):
    delivery = models.ForeignKey(DeliveryRegistrationRequests,on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=70)
    country = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    district = models.CharField(max_length=70)
    pincode = models.CharField(max_length=70)
    bank = models.CharField(max_length=70)
    acc_num = models.CharField(max_length=70)
    ifsc = models.CharField(max_length=70)

    def __str__(self):
        return self.delivery.user.first_name


class ProductSpeaker(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    battery = models.CharField(max_length=255, null=True) 
    s_connectivity = models.CharField(max_length=255, null=True)
    s_type = models.CharField(max_length=255, null=True)
    special_features = models.CharField(max_length=255, null=True)
    weight = models.CharField(max_length=255, null=True)
    charging = models.CharField(max_length=255, null=True)
    working = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return self.product.product_name
    
class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1) 
    
    def __str__(self):
        return self.product.product_name
    
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cartstock = models.PositiveIntegerField(default=1)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    # subtotal = models.IntegerField(default=0)
    # total = models.IntegerField(default=0)
    # def update_total(self):
    #     self.price = self.quantity * self.product.price
    
    def carttotal(self):
        self.cartstock = self.product.stock
    def __str__(self):
        return self.product.name
    

class Address(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    phone= models.IntegerField(max_length=12)
    pincode=models.IntegerField(max_length=6)
    locality=models.CharField(max_length=100)
    address=models.TextField(max_length=255, null=True, default=None)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=20)

    def __str__(self):
        return self.name + "-" + self.address


class Order(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255)
    # payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # currency = models.CharField(max_length=3)
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Cart)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    product_ids = models.ManyToManyField(Product,related_name='orders')
    delivery_order_status_choices = (
        ('pending','Pending'),
        ('picked_up','Picked Up'),
        ('delivered','Delivered')
    )
    delivery_order_status = models.CharField(max_length=20,choices=delivery_order_status_choices,default='pending')

    @property
    def product_names(self):
        product_names = ', ' .join([str(product) for product in self.product_ids.all()])
        return product_names

    def __str__(self):
        return f"Order for {self.user.first_name} | {self.product_names}" 

    class Meta:
        ordering = ['-timestamp']

class Delivery(models.Model):
    order=models.ForeignKey(Order,on_delete = models.CASCADE)  
    picked_up_at = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    delivered_at = models.DateTimeField(null=True,blank=True)
    delivery_agent = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='delivery_assignments')

    def __str__(self):
        return f"Deliver for Order {self.order.id}"
    
class payment(models.Model):
    class PaymentStatusChoices(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SUCCESSFUL = 'successful', 'Successful'
        FAILED = 'failed', 'Failed'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    cartstock = models.PositiveIntegerField(default=1)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.PENDING
    )
    
    def carttotal(self):
        self.cartstock = self.product.stock


class Book(models.Model):
    title=models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.title
    
