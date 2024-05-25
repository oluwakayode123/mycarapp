import requests
import uuid
import json


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator 
from django.contrib import messages     
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm   
from django.contrib.auth.decorators import login_required                                                                                  
from main.models import *
from .forms import *
# importing the AppInfo frommodels.py


# Create your views here.

def home(request):
    # info = AppInfo.objects.get(pk=1)

    categ = Category.objects.all()                                            
    # pk means primary key
    context = {
        # "info": info,
        "categ": categ
    }
    return render(request, 'index.html', context)


def products(request):
    product = Product.objects.all() 
    p = Paginator(product, 6)
    page = request.GET.get('page')
    pagin = p.get_page(page)

    context = {
        'pagin':pagin
    }
    return render(request, 'product.html', context)


def category(request, id, slug):
    carbrand = Category.objects.get(pk=id)
    caritem = Product.objects.filter(type_id = id)

    context = {
        'carbrand':carbrand,
        'caritem':caritem,
    }

    return render(request, 'category.html', context)


def detail(request, id, slug):
    cardet = Product.objects.get(pk=id)

    context = {
        'cardet':cardet
    }

    return render(request, 'detail.html', context)

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your message has been sent successfully!!!')
            return redirect('home')
        
    context = {
        'form':form
    }
        
    return render(request, 'contact.html', context)

def signout(request):
    logout(request)
    messages.success(request, 'you are now signed out')
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       if user:
           login(request, user)
           messages.success(request, 'login successful!')
           return redirect('home')
       else:
           messages.error(request, 'username/password is incorrect please try again')
           return redirect('signin')
       
    return render(request, 'login.html')


def register(request):
    register = CustomerForm()
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']
        pix = request.POST['pix']
        register = CustomerForm(request.POST)
        if register.is_valid():
            user = register.save()
            newuser =Customer(user=user)
            newuser.first_name = user.first_name
            newuser.last_name = user.last_name
            newuser.email = user.email
            newuser.phone = phone
            newuser.address = address
            newuser.pix = pix
            newuser.save()
            messages.success(request, f'dear {user.username} your account is created successfully')
            return redirect('signin')
        else:
            messages.error(request, register.errors)
    return render(request, 'register.html')


@login_required(login_url='signin')
def profile(request):
    userprof = Customer.objects.get(user__username = request.user.username)

    context = {
        'userprof':userprof
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    pform = ProfileForm(instance=request.user.customer)
    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=request.user.customer)
        if pform.is_valid():
            user = pform.save()
            new = user.first_name.title()
            messages.success(request, f'dear {new} profile update successful')
            return redirect ('profile')
        else:
            new = user.first_name.title()
            messages.error(request, f'dear {new} update not successful {pform.error}')
            return redirect('profile_update')
        
    context = {
        'userprof':userprof
    }

    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password_update(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        new = request.user.username.title()
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'dear {new} your password is now updated!!')
            return redirect('profile')    
        else:         
            messages.error(request, f'dear {new } error updating password, {form.errors}')  
            return redirect('password_update')

    context = {
        'userprof':userprof,
        'form':form
    }

    return render(request, 'password_update.html', context)

@login_required(login_url='signin')
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        carid = request.POST['carid']
        main = Product.objects.get(pk=carid)
        cart = Cart.objects.filter(user__username = request.user.username, paid=False)
        if cart:
            basket = Cart.objects.filter(user__username = request.user.username, paid=False, car=main.id, quantity=quantity).first()
            if basket:
                basket.quantity += quantity
                basket.amount = main.price * basket.quantity
                basket.save()
                messages.success(request,'one item added to cart')
                return redirect('products')
            else:
                newitem = Cart()
                newitem.user = request.user
                newitem.car = main
                newitem.quantity = quantity
                newitem.price = main.price
                newitem.amount = main.price * quantity
                newitem.paid = False
                newitem.save()
                messages.success(request, 'one item added to cart')
                return redirect('products')
        else:
            newcart = Cart()
            newcart.user = request.user
            newcart.car = main
            newcart.quantity = quantity
            newcart.price = main.price
            newcart.amount = main.price * quantity
            newcart.paid = False
            newcart.save()
            messages.success(request, 'one item added to cart')
            return redirect('products')

@login_required(login_url='signin')        
def cart(request):
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.quantity
        vat = 0.075 * subtotal
        total = subtotal * vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total
    }

    return render(request, 'cart.html', context)

def delete(request):
    if request.method == 'POST':
        del_item = request.POST['delid']
        Cart.objects.filter(pk=del_item).delete()
        messages.success(request, 'one item deleted')
        return redirect('cart')

@login_required(login_url='signin')
def update(request):
    if request.method == 'POST':
        qty_item = request.POST['quantid']
        new_qty = request.POST['quant']
        newqty = Cart.objects.get(pk=qty_item)
        newqty.quantity = new_qty
        newqty.amount = newqty.price * newqty.quantity
        newqty.save()
        messages.success(request, 'quantity updated')
        return redirect('cart')

@login_required(login_url='signin')
def checkout(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid=False)
    for item in cart:
        item.amount = item.price * item.quantity
        item.save()

    subtotal = 0
    vat = 0
    total = 0

    for item in cart:
        subtotal += item.price * item.quantity
        vat = 0.075 * subtotal
        total = subtotal + vat

    context = {
        'cart':cart,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
        'userprof':userprof,
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_3f2dfcec471be41dd7df788a039fd2237714b4c9'  #secret key from paystack
        curl = 'https://api.paystack.co/transaction/initialize'  #paystack call url
        cburl = 'http://127.0.0.1:8000/callback' #payment thankyou page
        ref = str(uuid.uuid4()) # ref no required by paystack for order number
        profile = Customer.objects.get(user__username = request.user.username)
        order_no =profile.id # main order number
        total = float(request.POST['total']) * 100 #total amount charged from customer card
        user =User.objects.get(username = request.user.username) #query the user model for customer details
        email = user.email #store customer email to send to paystack
        first_name = request.POST['first_name']#collect from the template incase of any change
        last_name = request.POST['last_name']#collect from the template incase of any change
        phone = request.POST['phone']#collect from the template incase of any change
        add_infoe = request.POST['add_info']#collect from the template incase of any change
        
        # collect data to send to paystack via call
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':ref, 'amount':int(total), 'email':user.email, 'callback_url':cburl, 'order_number':order_no, 'currency':'NGN'}

        #make a call to paystack
        try:
            r = requests.POST(curl, headers=headers, json=data)
        except Exception:
            messages.error(request, 'network bust, please try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.amount = total/100
            account.paid = True
            account.additional_info = add_info
            account.phone = phone
            account.pay_code = ref
            account.save()

            return redirect(rdurl)
    return redirect('checkout')


@login_required(login_url='signin')
def callback(request):
    userprof = Customer.objects.get(user__username = request.user.username)
    cart = Cart.objects.filter(user__username = request.user.username, paid = False)

    for item in cart:
        item.paid = True
        item.save()

        car = Product.objects.get(pk=item.car.id)

    context = {
        'userprof':userprof,
        'cart':cart,
        'car':car
    }
    return render(request, 'callback.html')







