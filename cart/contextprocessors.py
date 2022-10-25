
from account.models import Accounts
from cart.models import Cart
from django.contrib.auth import authenticate
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
        accountsid=Accounts.objects.get(username=name)
        allcartproduct=Cart.objects.filter(username_id=accountsid.id)

        for eachcartproduct in allcartproduct:
            totalamount1=totalamount1+eachcartproduct.product_id.price*eachcartproduct.totalquantity
        totalamount2=int(totalamount1)    
        tax=totalamount2*5/100
        tax=int(tax)
        finalamount =totalamount2+tax
        finalamountinRs=finalamount/82
        
        return dict(totalamount2=totalamount2,tax=tax,finalamount=finalamount,finalamountinRs=finalamountinRs)
    else:
        return {}