
from account.models import Accounts,Wallet
from cart.models import Cart
from django.contrib.auth import authenticate
from register.models import totalofferforuser

from store.models import Offers
def totalcartitems(request):
    count=0
    
    if request.user.is_authenticated:
        if request.user.is_admin==False:
            name=request.user.username
           
            accountsid    =Accounts.objects.get(username=name)
            allcartproduct=Cart.objects.filter(username_id=accountsid.id)

            for eachcartproduct in allcartproduct:
                count=count+eachcartproduct.totalquantity
            
            return dict(count=count)
        else:
            return {}
    else:
        return {}

def totalamount1(request):
    totalamount1=0
    if request.user.is_authenticated:
        name=request.user.username
        x=request.user
        offer=0
        totoff=None
        if x is not None and x.is_admin==False:
           allofferhedid= totalofferforuser.objects.filter(user=x)
           if allofferhedid : 
                totoff=allofferhedid[len(allofferhedid)-1]

        #totoff=totalofferforuser.objects.get(user=x)
        if totoff is not None:
            offer=totoff.totaloffer
        else:
            offer=0
        amount=0
        offers=Offers.objects.all()
        accountsid=Accounts.objects.get(username=name)
        allcartproduct=Cart.objects.filter(username_id=accountsid.id)
        if Wallet.objects.filter(user=x).exists():
            wallet=Wallet.objects.get(user=x)
            if wallet.amount !=0:
                amount=wallet.amount
                
            else:
                amount=0
        Realoffer=0
        for eachcartproduct in allcartproduct:

            if eachcartproduct.product_id.sellingprice==0 or eachcartproduct.product_id.sellingprice==eachcartproduct.product_id.price:
                totalamount1=totalamount1+eachcartproduct.product_id.price*eachcartproduct.totalquantity
            
            else:
                totalamount1=totalamount1+eachcartproduct.product_id.sellingprice*eachcartproduct.totalquantity
                diff=eachcartproduct.product_id.price-eachcartproduct.product_id.sellingprice
                Realoffer=Realoffer+diff

        totalamount2=int(totalamount1)    
        tax=totalamount2*5/100
        tax=int(tax)

        carttot=totalamount2+tax
        if int(offer)>5000:
            offer=5000

        finalamount =totalamount2+tax-offer-amount
        finalamountinRs=round(finalamount/82.82,2)
        #print("amount ",amount)
        return dict(Realoffer=Realoffer,totalamount2=totalamount2,tax=tax,finalamount=finalamount,finalamountinRs=finalamountinRs,offer=offer,carttot=carttot,amount=amount)
    else:
        return {}