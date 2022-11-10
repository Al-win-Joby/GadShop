from email.policy import default
from django.db import models
from account.models import Accounts

from cart.models import Cart
from store.models import Offers
class UserObtainedOffer1(models.Model):
    cart                  =models.ForeignKey(Cart,on_delete=models.CASCADE)
    offer                 =models.ForeignKey(Offers,on_delete=models.CASCADE)
    offerpricereduced     = models.IntegerField()

class totalofferforuser(models.Model):
    totaloffer=models.IntegerField(default=0)
    user      =models.ForeignKey(Accounts,on_delete=models.CASCADE)