 
from email.policy import default
from itertools import product
from tkinter.tix import Tree
from django.db import models
from django.urls import reverse
#from account.models import Accounts
from category.models import Category, Subcategory

# Create your models here.
class Products(models.Model):
    product_name    =models.CharField(max_length=200,unique=True)
    slug            =models.SlugField(max_length=200,unique=True)
    desciption      =models.TextField(max_length=200,blank=True)
    price           =models.IntegerField()
    sellingprice    =models.IntegerField(default=0)
    images          =models.ImageField(upload_to='photos/store')
    stock           =models.IntegerField()
    is_available    =models.BooleanField(default=True)
    category_name        =models.ForeignKey(Category,on_delete=models.CASCADE)
    subcategory_name     =models.ForeignKey(Subcategory,on_delete=models.CASCADE)
                    
    created_date    =models.DateTimeField(auto_now_add=True)
    modified_date   =models.DateTimeField(auto_now_add=True)

    def geturl(self):
        
        return reverse('showproduct',args=[self.category_name.slug,self.slug])

    def __str__(self):
        return self.product_name

    def afteroffer(self):
        alloffers=RealOffers.objects.all()
       
        x=1
        price=self.price
        for i in alloffers:            
            if(i.product==self):
                print("prod")
                if x>(100-int(i.offerpercentage))/100:
                    x=(100-int(i.offerpercentage))/100
                    price=i.product.price*x
                          
            elif(i.subcategory==self.subcategory_name):
                
                if x>(100-int(i.offerpercentage))/100:
                    x=(100-int(i.offerpercentage))/100     
                    
                    price=self.price*x                


            elif(i.category==self.category_name) :
                print("cat")
                if x>(100-int(i.offerpercentage))/100:
                    x=(100-int(i.offerpercentage))/100
                    price=self.price*x

        if self.price-int(price)>5000:        
            price=self.price-5000

        
        if x==1:
            price=self.price

        price=int(price)

        self.sellingprice=int(price)
        self.save()
        return True

class additionalimage(models.Model):
    images          =models.ImageField(upload_to='photos/store')
    product         =models.ForeignKey(Products,on_delete=models.CASCADE)

class Offers(models.Model):      #This is for coupon
    code            =models.CharField(max_length=200)
    offerpercentage =models.IntegerField()
    category        =models.ForeignKey(Category,on_delete=models.CASCADE,blank=True, null=True)
    subcategory     =models.ForeignKey(Subcategory,on_delete=models.CASCADE,blank=True, null=True)
    product         =models.ForeignKey(Products,on_delete=models.CASCADE,blank=True, null=True)

class RealOffers(models.Model):
    offername        =models.CharField(max_length=200)
    offerpercentage =models.IntegerField()
    category        =models.ForeignKey(Category,on_delete=models.CASCADE,blank=True, null=True)
    subcategory     =models.ForeignKey(Subcategory,on_delete=models.CASCADE,blank=True, null=True)
    product         =models.ForeignKey(Products,on_delete=models.CASCADE,blank=True, null=True)


