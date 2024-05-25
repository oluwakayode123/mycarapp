from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AppInfo(models.Model):
    appname = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logo')
    carousel1 = models.ImageField(upload_to='carousel1')
    carousel2 = models.ImageField(upload_to='carousel2')
    carousel3 = models.ImageField(upload_to='carousel3')
    carousel4 = models.ImageField(upload_to='carousel4')
    banner = models.ImageField(upload_to='banner')
    copyright = models.IntegerField()

    def __str__(self):
        return self.appname
    
class Category(models.Model):
    brand = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    pix = models.ImageField(upload_to='pix')

    def __str__(self):
        return self.brand

class Product(models.Model):
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=50,)                           
    year = models.IntegerField()
    seats = models.IntegerField()
    registered = models.BooleanField()
    price = models.IntegerField()
    promo_price = models.IntegerField(blank=True, null=True)
    carimg = models.ImageField(upload_to='carimg')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.model

class Contact(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField(max_length=100)
    sent = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    pix = models.ImageField(upload_to='customer')

    def __str__(self):
        return self.user.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField()
    paid = models.BooleanField()
    amount = models.CharField(max_length=50)

    def __sttr__(self):
        return self.user.username 
    
class Payment(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    amount = models.IntegerField()
    paid = models.BooleanField()
    phone = models.CharField(max_length=50)
    pay_code = models.CharField(max_length=50)
    additional_info = models.TextField()
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


