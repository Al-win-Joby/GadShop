from email.policy import default
from django.db import models

from account.models import Accounts
from store.models import Products
# Create your models here.
class Cart(models.Model):
    username_id=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    totalquantity=models.IntegerField(default=0)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)

    def gettotprice(self):
        if self.product_id.sellingprice==0 or self.product_id.sellingprice==self.product_id.price:
            return self.product_id.price*self.totalquantity

        else:
            return self.product_id.sellingprice*self.totalquantity 