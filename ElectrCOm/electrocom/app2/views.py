from decimal import Decimal
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.db import transaction
# from .forms import ProductForm,SpecificationForm

from django.contrib  import messages,auth
# from .models import Brand, Category, CustomUser, Product
from .models import Address, CustomUser, Order, Product, ProductHeadset, ProductLap, ProductMobile,Profile,SellerProfile,Delivery
from .models import sellerRegistrationRequest, DeliveryRegistrationRequests,DeliveryProfile, ProductSpeaker,Cart, Wishlist
# from accounts.backends import EmailBackend
from django.contrib.auth import get_user_model
#from .forms import UserForm, ServiceForm 
from django.db.models import Q,Sum

User = get_user_model()

# Create your views here.

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('pass', None)
        role = 1
        print(email)

        if first_name and last_name and email and role and password:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'register.html', {'error_message': error_message})
            
            else:
                user = User(first_name = first_name, last_name=last_name, email=email, role=role)
                # profile = Profile(user=user)
                user.set_password(password)  # Set the password securely
                user.save()
                # profile.save()
                return redirect('login')  
            
    return render(request, 'register.html')

def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')
       

        if not email or not password:
            error_message = "please provide details to login in"
            return render(request, 'login.html', {'error_message': error_message})
        
        user = authenticate(request, email=email, password=password)
            
        if user is not None:
            auth_login(request, user) 
            if user.role == 2:       
                return redirect('sellerDashboard')
            elif user.role == 3:       
                return redirect('delivery_form2')
            else:
                return redirect('/')
            
        else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
            
    return render(request,'login.html')

def userLogout(request):
    auth.logout(request)
    request.session.pop('is_logged_in',None)
    return redirect('/') 

def delLogout(request):
    auth.logout(request)
    request.session.pop('is_logged_in',None)
    return redirect('login')
            
@login_required(login_url='/app2/login')
def profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile=None
        
    if request.method == "POST":
        if profile is None:
            profile = Profile(user=user)
        profile.district = request.POST.get('district')
        profile.state = request.POST.get('state')
        profile.country = request.POST.get('country')
        profile.address = request.POST.get('address')
        profile.pincode = request.POST.get('pincode')

        profile.save()
            
        return redirect('profile')
    
    return render(request,'profile.html',{'user':user,'profile':profile})

def seller_registration(request):
    
    if request.method == 'POST':
        gst = request.POST.get('gst')
        pan = request.POST.get('pan')

        # Validate the form data
        if not gst or not pan:
            # Handle invalid data
            return render(request, 'sellerreg.html',{'error': 'Please enter both GST IN and PAN'})

        # Create a seller registration request object
        registration_request = sellerRegistrationRequest(
            user=request.user,
            gst=gst,
            pan=pan
        )
        registration_request.save()
        return redirect('/')

        # Send notification to admin about the new request
    if request.user.role == 2:
        return render(request, 'sellerDashboard.html')
    else:
        return render(request,'sellerreg.html')


def delivery_registration(request):
    print("Function")
    if request.method == 'POST':
        print("submited")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        # confirm_password = request.POST.get('confirm')
        
        if CustomUser.objects.filter(email=email).exists():  
            print("already")          
            messages.error(request,'email already exists')
        
        # elif password != confirm_password:
        #     print("pass")
        #     messages.error(request,'Password doesnot match')
        elif first_name and last_name and email and password:
            user=CustomUser(first_name=first_name,last_name=last_name,email=email,role = 3)
            user.set_password(password)
            user.is_active = True
            user.save()
            print("hai")

        return redirect('login')
    return render(request,"delivery/del_reg.html")

def login(request):
    return render(request,'userlogin')

@login_required(login_url='/app2/login')
def delivery_form2(request):
    user=request.user
    try:
        try:
            currentUser=DeliveryRegistrationRequests.objects.get(user=user)
        except:
            currentUser=None
        print(currentUser)
        if currentUser:
            if currentUser.status=="PENDING":
                return render(request,"delivery/waiting.html") # create a waiting page
            elif currentUser.status=='APPROVED':
                return redirect('delivery_index')
        else:
            if request.method == 'POST':
                rc_num = request.POST.get('rc_num')
                lic_num = request.POST.get('lic_num')
                aadhar_num = request.POST.get('aadhar_num')
                pan = request.POST.get('pan')

                if not rc_num and not lic_num and not aadhar_num and not pan:
                    return render(request,"delivery_form2.html",{'error':'enter details'})

                registration_request = DeliveryRegistrationRequests(
                    user=request.user,
                    rc_num=rc_num,
                    lic_num=lic_num,
                    aadhar_num=aadhar_num,
                    pan=pan

                    )
                registration_request.save()
                print("success")
                return redirect('waiting') #After create a waiting page
    except ObjectDoesNotExist:
        print("DeliveryRegistrationRequests does not exist for the current user")
        
    return render(request, 'delivery/delivery_form2.html')


def waiting(request):
    return render(request,'delivery/waiting.html')   

@login_required(login_url='/app2/login')
def delivery_index(request):
    user=request.user.id
    return render(request,'delivery/delivery_index.html')

@login_required(login_url='/app2/login')
def arrivals(request):
    user=request.user
    successfull_orders = Order.objects.filter(payment_status=Order.PaymentStatusChoices.SUCCESSFUL)
    unique_addresses=[]
    for order in successfull_orders:
        if order.address:
            if order.address not in unique_addresses:
                unique_addresses.append(order.address)
    order_products={}
    for order in successfull_orders:
        products = [item.product_name for item in order.items.all()]
        order_products[order]=products    
    context = {
        'unique_addresses': unique_addresses,
        'order_products': order_products
    }
    # print(order_products)

    return render(request,'delivery/arrivals.html',context)


@login_required(login_url='/app2/login')
def delivery_profile(request):
    # Fetch DeliveryRegistrationRequests object for the current user
    data = DeliveryRegistrationRequests.objects.get(user=request.user)

    # Fetch or create DeliveryProfile object for the current user
    profile, created = DeliveryProfile.objects.get_or_create(delivery=data)

    if request.method == 'POST':
        # Update the existing profile with the new data
        profile.address = request.POST.get('address')
        profile.country = request.POST.get('country')
        profile.state = request.POST.get('state')
        profile.district = request.POST.get('district')
        profile.pincode = request.POST.get('pincode')
        profile.bank = request.POST.get('bank')
        profile.acc_num = request.POST.get('acc_num')
        profile.ifsc = request.POST.get('ifsc')
        profile.save()
        print("Profile updated successfully")

    return render(request, 'delivery/deliveryProfile.html', {'all': data, 'profile': profile})


from django.core.exceptions import ObjectDoesNotExist 

def sellerProfile(request):
    user = request.user

    # Check if the user is an approved seller
    # if user.role != 2:
    #     return redirect('home')
    try:
        data = SellerProfile.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        data = None
    try:
        profile = Profile.objects.get(user_id=user.id)
    except ObjectDoesNotExist:
        profile = None
        
    return render(request, 'sellerProfile.html', {'data': data, 'profile': profile})

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=sellerRegistrationRequest)
def process_approved_requests(sender, instance, created, **kwargs):
    if instance.status == 'APPROVED':
        # Update the user's role to 'seller'
        instance.user.role = 2
        instance.user.save()

        # Create a SellerProfile object for the approved seller
        SellerProfile.objects.create(user=instance.user, gst=instance.gst, pan=instance.pan)

from django.contrib.sessions.models import Session

def process_approved_requests(sender, instance, created, **kwargs):
    if instance.status == 'APPROVED':
        # Update the user's role to 'seller'
        instance.user.role = 2
        instance.user.save()

        # Create a SellerProfile object for the approved seller
        SellerProfile.objects.create(user=instance.user, gst=instance.gst, pan=instance.pan)

        # Set a session variable indicating the user is a new seller
        session = Session.objects.get(session_key=instance.user.session_key)
        session['new_seller'] = True
        session.save()

# def process_approved_requests(sender,instance,created,*kwargs):
#     if instance.status == 'APPROVED':
#         instance.user.role = 3
#         instance.user.save()

#         DeliveryProfile.objects.create(user=instance.user,id_num=instance.id_num,license_num=instance.license_num)

#         session = Session.objects.get(session_key=instance.user.session_key)
#         session['new_delivery']=True
#         session.save()



def sellerindex(request):
    return render(request,'sellerindex.html')

def sellerlogin(request): 
    return render(request,'sellerlogin.html')

# new Product

def addProduct(request):
    user = request.user
    userid = user.id
    if request.method == 'POST':
        newproduct = Product(
        user = userid,
        name = request.POST.get('name'),
        brand_name = request.POST.get('brand_name'),
        product_name = request.POST.get('product_name'),
        price = request.POST.get('price'),
        image1 = request.POST.get('image1'),
        image2 = request.POST.get('image2'),
        image3 = request.POST.get('image3'),
        description = request.POST.get('description'),
        stock = request.POST.get('stock'),
        category = request.POST.get('category'),
        
        )
        newproduct.save()
        
        return redirect("/")
    return render(request,'addproduct.html')

def regheadset(request):
    print("headset")
    user = request.user
    userid = user.id
    if request.method == 'POST':
        newproduct = Product(
        user_id = userid,
        name = request.POST.get('name'),
        brand_name = request.POST.get('brandName'),
        product_name = request.POST.get('productName'),
        price = request.POST.get('price'),
        image1 = request.FILES.get('image1'),
        image2 = request.FILES.get('image2'),
        image3 = request.FILES.get('image3'),
        description = request.POST.get('description'),
        stock = request.POST.get('stock'),
        
        category = 'headset'
        
        )
        newproduct.save()
        headset_id=newproduct.id
        headset_obj = ProductHeadset(
            product_id=headset_id,
        )
        headset_obj.save()
        
        return redirect("/")
    return render(request,'product_form.html')

def regmobile(request):
    print("mobile")
    user = request.user
    userid = user.id
    if request.method == 'POST':
        newproduct = Product(
        user_id = userid,
        name = request.POST.get('name'),
        brand_name = request.POST.get('brandName'),
        product_name = request.POST.get('productName'),
        price = request.POST.get('price'),
        image1 = request.FILES.get('image1'),
        image2 = request.FILES.get('image2'),
        image3 = request.FILES.get('image3'),
        description = request.POST.get('description'),
        stock = request.POST.get('stock'),
        category = 'mobile'
        
        )
        newproduct.save()
        mobile_id=newproduct.id
        mobile_obj = ProductMobile(
            product_id=mobile_id,
        )
        mobile_obj.save()
        
        return redirect("/")
    return render(request,'product_form2.html')

def reglaptop(request):
    user = request.user
    userid = user.id
    if request.method == 'POST':
        newproduct = Product(
        user_id = userid,
        name = request.POST.get('name'),
        brand_name = request.POST.get('brandName'),
        product_name = request.POST.get('productName'),
        price = request.POST.get('price'),
        image1 = request.FILES.get('image1'),
        image2 = request.FILES.get('image2'),
        image3 = request.FILES.get('image3'),
        description = request.POST.get('description'),
        stock = request.POST.get('stock'),
        category = 'laptop'
        
        )
        newproduct.save()
        laptop_id=newproduct.id
        laptop_obj = ProductLap(
            product_id=laptop_id,
        )
        laptop_obj.save()
        
        return redirect("/")
    return render(request,'product_form3.html')

def regspeaker(request):
    user = request.user
    userid = user.id
    if request.method == 'POST':
        newproduct = Product(
        user_id = userid,
        name = request.POST.get('name'),
        brand_name = request.POST.get('brandName'),
        product_name = request.POST.get('productName'),
        price = request.POST.get('price'),
        image1 = request.FILES.get('image1'),
        image2 = request.FILES.get('image2'),
        image3 = request.FILES.get('image3'),
        description = request.POST.get('description'),
        stock = request.POST.get('stock'),
        category = 'speaker'
        
        )
        newproduct.save()
        speaker_id=newproduct.id
        speaker_obj = ProductSpeaker(
            product_id=speaker_id,
        )
        speaker_obj.save()
        
        return redirect("/")
    return render(request,'product_form4.html')

def addlaptop(request,product_id):
    user = request.user
    userid = user.id
    laptop = ProductLap.objects.get(product_id=product_id)
    if request.method == 'POST':
        print(laptop)
        laptop.screen_size = request.POST.get('screen_size')
        laptop.storage = request.POST.get('storage')
        laptop.processor = request.POST.get('processor')
        laptop.ram = request.POST.get('ram')
        laptop.os = request.POST.get('os')
        laptop.graphics = request.POST.get('graphics')
        laptop.color = request.POST.get('color')
        laptop.stock = request.POST.get('stock')
        print(laptop)
        laptop.save()   
        
        return redirect("/")
    return render(request,'addproduct/laptop.html',{'laptop':laptop})

def addmobile(request,product_id):
    user = request.user
    userid = user.id
    mobile = ProductMobile.objects.get(product_id=product_id)
    if request.method == 'POST':
        print(mobile)
        # Create a new Category instance and assign values
        mobile.wireless=request.POST.get('wireless')
        mobile.m_os=request.POST.get('m_os')
        mobile.cellular=request.POST.get('cellular')
        mobile.memory=request.POST.get('memory')
        mobile.connectivity=request.POST.get('connectivity')
        mobile.m_screen=request.POST.get('m_screen')
        mobile.wireless_network_technology=request.POST.get('wireless_network_technology')
        mobile.color=request.POST.get('color')
        mobile.ram=request.POST.get('ram')
        mobile.processor=request.POST.get('processor')
        mobile.camrear=request.POST.get('camrear')
        mobile.camfront=request.POST.get('camfront')
        mobile.stock = request.POST.get('stock')
        
        print(mobile)
        mobile.save()  
        
        return redirect("/")
    return render(request, 'addproduct/mobile.html',{'mobile':mobile})

def addheadset(request,product_id):
    user = request.user
    userid = user.id
    head=ProductHeadset.objects.get(product_id=product_id)
    if request.method == 'POST':
        head.battery = request.POST.get('battery')
        head.color = request.POST.get('color')
        head.form_factor = request.POST.get('form_factor')
        head.h_connectivity = request.POST.get('h_connectivity')
        head.weight = request.POST.get('weight')
        head.charging = request.POST.get('charging')
        head.working = request.POST.get('working')
        head.stock = request.POST.get('stock') 
        print(head)
        head.save()   
        
        return redirect("/")
    return render(request,'addproduct/headset.html',{'head':head})

def addspeaker(request,product_id):
    user = request.user
    userid = user.id
    speaker=ProductSpeaker.objects.get(product_id=product_id)
    if request.method == 'POST':
        print(speaker)
        # Create a new Category instance and assign values
        speaker.battery = request.POST.get('battery')
        speaker.s_connectivity = request.POST.get('s_connectivity')
        speaker.s_type = request.POST.get('s_type')
        speaker.special_features = request.POST.get('special_features')
        speaker.weight = request.POST.get('weight')
        speaker.charging = request.POST.get('charging')
        speaker.working = request.POST.get('working')
        
        print(speaker)
        speaker.save()   
        
        return redirect("/")
    return render(request,'addproduct/speaker.html',{'speaker':speaker})

def mobile_list(request):
    data = ProductMobile.objects.all()
    user= request.user
    return render(request,'products/mobile.html',{'data':data})


def viewHeadset(request):
    data = Product.objects.filter(user_id=request.user.id,category='headset')
    user= request.user
    return render(request,'products/headset.html',{'data':data})

def viewSpeaker(request):
    data = Product.objects.filter(user_id=request.user.id,category='speaker')
    user= request.user
    return render(request,'products/speaker.html',{'data':data})

def viewMobile(request):
    data = Product.objects.filter(user_id=request.user.id,category='mobile')
    user= request.user
    return render(request,'products/mobile.html',{'data':data})

def viewLaptop(request):
    data=Product.objects.filter(user_id=request.user.id,category='laptop')
    user = request.user
    return render(request,'products/laptop.html',{'data':data})

def laptop_list(request):
    data=ProductLap.objects.all()
    user = request.user
    return render(request,'products/laptop.html',{'data':data})

def headset_list(request):
    data = ProductHeadset.objects.all()
    user = request.user
    return render(request,'products/headset.html',{'data':data})

def speaker_list(request):
    data = ProductSpeaker.objects.all()
    user = request.user
    return render(request,'products/speaker.html',{'data':data})


def headset_details(request,product_id):
    products = Product.objects.filter(id=product_id)
    headset = ProductHeadset.objects.get(product_id=product_id)
    return render(request,'details/headset.html',{'product':products,'headset':headset})

def speaker_details(request,product_id):
    product = Product.objects.filter(id=product_id)
    speaker = ProductSpeaker.objects.get(product_id=product_id)
    return render(request,'details/speaker.html',{'product':product,'speaker':speaker})

def laptop_details(request,product_id):
    product = Product.objects.filter(id=product_id)
    laptop = ProductLap.objects.get(product_id=product_id)
    return render(request,'details/laptop.html',{'product':product,'laptop':laptop})

def mobile_details(request,product_id):
    product = Product.objects.filter(id=product_id)
    mobile = ProductMobile.objects.get(product_id=product_id)
    return render(request,'details/mobile.html',{'product':product,'mobile':mobile})

def sellerDashboard(request):  
    return render(request,'sellerDashboard.html')

def product_form(request):
    return render(request,'product_form.html')

def allproducts(request):
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(name__icontains=q) | Q(product_name__icontains=q) | Q(price__icontains=q) | Q(category__icontains = q))
        data = Product.objects.filter(multiple_q)
    else:
        data = Product.objects.all()
    return render(request,'products/allproducts.html',{'data': data})

def product_details(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    specific_product = None
    if product.category == 'mobile':
        specific_product = get_object_or_404(ProductMobile, product=product)
        # return render(request, 'details/mobile.html', {'product': product, 'specific_product': specific_product})
    elif product.category == 'headset':
        specific_product = get_object_or_404(ProductHeadset, product=product)
        # return render(request, 'details/mobile.html', {'product': product, 'specific_product': specific_product})
    elif product.category == 'speaker':
        specific_product = get_object_or_404(ProductSpeaker, product=product)
        # return render(request, 'details/mobile.html', {'product': product, 'specific_product': specific_product})
    elif product.category == 'laptop':
        specific_product = get_object_or_404(ProductLap, product=product)
        # return render(request, 'details/mobile.html', {'product': product, 'specific_product': specific_product})    
    else:
        specific_product = None
    return render(request, 'details/allproducts.html', {'product': product, 'specific_product': specific_product})

def addtowishlist(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    wish_item, created = Wishlist.objects.get_or_create(product_id=product_id,user_id = request.user.id)
    
    if not created:
        wish_item.quantity += 1
        wish_item.save()
    else:
        wish_item.price = product.price
        wish_item.save()
    return redirect('wishlist')

def removewishlist(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = get_object_or_404(Wishlist, product=product, user=request.user)
    wishlist_item.delete()
    
    return redirect('wishlist')

def wishlist(request):
    wish = Wishlist.objects.filter(user_id=request.user.id)
    is_empty = not wish.exists()
    if is_empty:
        messages.warning(request, f"Your wishlist is empty.")

    return render(request,'wishlist.html',{'wish':wish,'is_empty':is_empty})

@login_required(login_url='/app2/login')
def addtocart(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    print(product.stock)

    quantity = product.stock
    cart_item, created = Cart.objects.get_or_create(product_id=product_id,user_id = request.user.id)
   
    if created:
        if product.stock > 0:
            cart_item.price = product.price
            cart_item.save()
            product.stock -= 1
            product.save()
        else:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
    return redirect('cart')

def delete_cart(request,product_id):
    cart_item = Cart.objects.filter(id=product_id)
    for cart_item in cart_item:
        product = cart_item.product
        deleted_quantity = cart_item.quantity
        cart_item.delete()
        product.stock += deleted_quantity
        product.save()
    return redirect('cart')


@login_required(login_url='/app2/login')
def cart(request):
    product = Cart.objects.filter(user_id=request.user.id)
    product_name = set(item.product.product_name for item in product)
    sub_total = sum([item.price * item.quantity for item in product])
    total_price = sub_total
    is_empty = not product.exists()
    
    if product.exists():
        print(product_name)
    # cartstock = Cart.objects.filter(user_id=request.user.id)
    if is_empty:
        messages.warning(request, f"Your cart is empty.")
    context = {
        'product':product,
        'total_price':total_price,
        'sub_total':sub_total,
        'is_empty':is_empty
        }
    return render(request,'cart.html',context)


def increase_item(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id)

        if cart_item.product.stock > 0:
            cart_item.quantity += 1
            cart_item.save()

            # Decrease stock in Product model
            cart_item.product.stock -= 1
            cart_item.product.save()
        else:
            messages.warning(request, f"{cart_item.product.product_name} is out of stock.")
    except Cart.DoesNotExist:
        pass

    return redirect('cart')

def decrease_item(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

            cart_item.product.stock += 1
            cart_item.product.save()
        else:
            messages.warning(request, f"{cart_item.product.product_name} cannot be removed.")
    except Cart.DoesNotExist:
        pass

    return redirect('cart')

@login_required(login_url='/app2/login')
def get_user_address(user):
    return user


@login_required(login_url='/app2/login/')
def orders(request):
    cart = Cart.objects.filter(user_id = request.user.id)
    total_quantity = cart.aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    product_name = set(item.product.product_name for item in cart)
    sub_total = sum(item.price*item.quantity for item in cart)
    total_price = sub_total
    added = total_price+60
    is_empty = not cart.exists()
    try:
        address = Address.objects.filter(user=request.user)
        # address_id = address.id
    except Address.DoesNotExist:
        address=None

    if not address:
        print("no address")

    if is_empty:
        messages.warning(request,"Your cart is empty")
        return redirect('cart')

    context = {
        'cart' : cart,
        'address':address,
        # 'address_id':address_id,
        'product_name':product_name,
        'total_quantity':total_quantity,
        'sub_total':sub_total,  
        'total_price': total_price,
        'sum':added,
        'address' : address
    }
    print(total_quantity)

    for order in Order.objects.all():
        for cart in order.items.all():
            product_id = cart.product.id
            print(product_id)

    return render(request,'order.html',context)

def accepted(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        order_id = request.POST.get('order_id')
        try:
           order = Order.objects.get(pk=order_id)
           order.delivery_order_status='picked_up'

           delivery,created = Delivery.objects.get_or_create(order=order)
           delivery,picked_up_at = timezone.now()

           order.save()
           delivery.save()
           messages.success(request,'Order successfully picked up')
           print(messages.success(request,'Order successfully picked up'))
        except Order.DoesNotExist:
            messages.error(request,'Order not found')
            print(messages.error(request,'Order not found'))
        except Exception as e:
            messages.error(request,f'an error occured: {e}')
            print(messages.error(request,f'an error occured: {e}'))
        return redirect('orders')

    return render(request,'delivery/accepted.html')


@login_required(login_url='/app2/login/')
def address(request):
    user = request.user.id
    view = Address.objects.filter(user_id = request.user.id)
    addresses = Address.objects.filter(user=request.user)

    if request.method=='POST':
        add = Address(
            user = request.user,
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            pincode = request.POST.get('pincode'),
            locality = request.POST.get('locality'),
            address = request.POST.get('address'),
            city = request.POST.get('city'),
            state = request.POST.get('state'),
        )
        add.save()

    context = {
        'addresses': addresses
    }
        
    return render(request,'address.html',context)

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
def payment(request):
    cart = Cart.objects.filter(user_id=request.user)
    address= Address.objects.get(user_id=request.user.id)
    currency = 'INR'
    sub_total = sum([item.product.price * item.quantity for item in cart])
    total_price = Decimal(sub_total+60)
    amount = int(total_price * 100)
    print(address)
    print("product")
    product_ids = [item.product.id for item in cart]
    # address = get_user_address(request.user)
    print(address)
    
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    razorpay_order_id = razorpay_order['id']
    from django.urls import reverse


    callback_url = reverse('paymenthandler')
    
    order = Order.objects.create(
        user = request.user,
        amount = total_price,
        razorpay_order_id = razorpay_order_id,
        payment_status = Order.PaymentStatusChoices.PENDING,
        address_id = address.id,
    )
    order.product_ids.set(product_ids)
    
    for cart in cart:
        order.items.add(cart)
    
    order.save()
    print(order)
 
    
    context = {
        'cart': cart,
        'amount': total_price,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,  # Set to 'total_price'
        'currency': currency,
        'callback_url': callback_url,
    }
        # context['razorpay_order_id'] = razorpay_order_id
        # context['total_price'] = total_price
        # context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        # context['razorpay_amount'] = amount
        # context['currency'] = currency
        # context['callback_url'] = callback_url
    
    return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    print("paymenthandler")
    if request.method == "POST":
            address_id = request.POST.get('address_id') 
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
                'address_id':address_id,
            }
 
          
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                 with transaction.atomic():
                    payment = Order.objects.get(razorpay_order_id= razorpay_order_id)
                    amount=int(payment.amount*100)
                #  razorpay_order = razorpay_client.order.fetch(razorpay_order_id)
                #  authorized_amount = razorpay_order['amount']
    
                    for order_item in payment.items.all():
                        product = order_item.product
                        if product.stock < order_item.quantity:
                            return render(request,'paymentfail.html',{'messages':'insufficient stock'})

                    razorpay_client.payment.capture(payment_id, amount)
                    payment.payment_id = payment_id
                    payment.payment_status = payment.PaymentStatusChoices.SUCCESSFUL
                    payment.save()

                    for order_item in payment.items.all():
                        product = order_item.product
                        product.stock -= order_item.quantity
                        product.save()

                    cart_items=Cart.objects.filter(user_id=request.user.id)
                    cart_items.delete()
                 
                 return redirect('http://127.0.0.1:8000/')
                
            else:
 
                
                return render(request, 'paymentfail.html')
    else:
       
        return HttpResponseBadRequest()



# def product_search(request):
#     query = request.GET.get('q')
#     print(query)
#     if query:
#         result = Product.object.filter(name__icontains=query)
#     else:
#         result = Product.objects.none()

#     html = render_to_string('search_results.html',{'result':result,'query':query})
#     return JsonResponse
        