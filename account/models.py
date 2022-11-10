import code
from datetime import date
from itertools import product
from telnetlib import STATUS
from unicodedata import category
from django.db import models

# Create your models here.
import email
from email.policy import default

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from category.models import Category, Subcategory

from store.models import Products
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,phone_number,username,email,password=None):
        # if not email:
        #     raise ValueError("Email Required")
        
        # if not username:
        #     raise ValueError("Username Required")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self,first_name,last_name,email,phone_number,username,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
class Accounts(AbstractBaseUser):
    first_name      =models.CharField(max_length=200)
    last_name       =models.CharField(max_length=200)
    username        =models.CharField(max_length=200,unique=True)
    email           =models.EmailField(max_length=200,unique=True)
    phone_number    =models.CharField(max_length=200)

    date_joined         =models.DateTimeField(auto_now_add=True)
    last_login          =models.DateTimeField(auto_now_add=True)
    is_admin            =models.BooleanField(default=False)
    is_staff            =models.BooleanField(default=True)
    is_superadmin       =models.BooleanField(default=False)

    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['username','first_name','last_name','phone_number']
    
    objects= MyAccountManager()
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None ):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

class Address(models.Model):
    username_id=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    country=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    street=models.CharField(max_length=200)
    building_number=models.IntegerField()
    housename   =models.CharField(max_length=200)
    pincode     =models.IntegerField()

    def fulladd(self):
        fulladd=self.housename+","+self.street
        return fulladd

class Orders(models.Model):
    quantity    =models.IntegerField()
    date        =models.DateTimeField(auto_now_add=True)
    status      =models.CharField(max_length=200)
    user        =models.ForeignKey(Accounts,on_delete=models.CASCADE)
    product     =models.ForeignKey(Products,on_delete=models.CASCADE)
    Address     =models.ForeignKey(Address,on_delete=models.CASCADE)
    price       =models.IntegerField(default=0)

    def total(self):        
        x=int(self.price)*int(self.quantity)       
        return x

class Referrel(models.Model):
    code    =   models.CharField(max_length=200)
    user    =   models.ForeignKey(Accounts,on_delete=models.CASCADE)
    referredto=models.CharField(max_length=200,default=0)

class Wallet(models.Model):
    user    = models.ForeignKey(Accounts,on_delete=models.CASCADE)
    amount  = models.IntegerField(default=0)