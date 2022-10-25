from django.urls import reverse
from email.policy import default
from enum import unique
from this import d
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class Category(models.Model):
    category_name   =models.CharField(max_length=50,unique=True)
    slug            =models.SlugField(max_length=100,unique=True)
    category_image  =models.ImageField(upload_to='photos/category',blank=True)
    description     =models.TextField(max_length=200,blank=True)
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    
    def geturl(self):
        return reverse('filteredhome',args=[self.slug])

    def __str__(self):
        return self.category_name

class Subcategory(models.Model):
    subcategory_name  =models.CharField(max_length=50,unique=True)
    slug              =models.CharField(max_length=100,unique=True)
    category_name     =models.ForeignKey(Category,on_delete=models.CASCADE)
    class Meta:
        verbose_name='Subcategory'
        verbose_name_plural='Sub categories'
    
    def __str__(self):
        return self.subcategory_name