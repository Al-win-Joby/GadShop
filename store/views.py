from ast import keyword
from multiprocessing import context
from sre_constants import SUCCESS
from unicodedata import category
from urllib import request, response
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache

from django.contrib import messages
from account.models import Accounts, Address,Orders,Referrel,Wallet
from cart.models import Cart
from register.models import UserObtainedOffer1, totalofferforuser
import xlwt
from django.http import HttpResponse
from store.models import Products, RealOffers, additionalimage,Offers
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import re
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from category.models import Category,Subcategory
# Create your views here.
def adminproduct(request):
    name= request.user.username
    listofproduct=Products.objects.all().order_by('-created_date')
    paginator=Paginator(listofproduct,8)
    page=request.GET.get('page')
    pagedproduct=paginator.get_page(page)
    context={'name':name,'listofproducts':pagedproduct}
    return render(request,'adminproduct.html',context)

def addproduct(request):
    name= request.user.username
    categories=Category.objects.all()
    
    subcategories=Subcategory.objects.all()
    print(subcategories)
    context={'name':name,'categories':categories,'subcategories':subcategories}
    return render (request,'addproduct.html',context)

def selectitem(request,x):
    print(x)
    if x=="category":
        item=Category.objects.all()

    elif x=="subcategory":
        print("subs")
        item=Subcategory.objects.all()
    else:
        item=Products.objects.all()
    #subcat=Subcategory.objects.filter(category_name=x)
    return render(request,'suboffer.html',{'subcat':item,'x':x})

def subcataddproduct(request,catid):
    print(catid)
    subcat=Subcategory.objects.filter(category_name=catid)
    return render(request,'subcat.html',{'subcat':subcat})

def addthisproduct(request):
    newproduct=Products()
    print("inside addthis produc")
    productname=request.POST.get('productname')
    newproduct.product_name=request.POST.get('productname')
    newproduct.slug=request.POST.get('productname')

    newproduct.slug = newproduct.slug.lower().strip()
    newproduct.slug = re.sub(r'[^\w\s-]', '', newproduct.slug)
    newproduct.slug = re.sub(r'[\s_-]+', '-', newproduct.slug)
    newproduct.slug = re.sub(r'^-+|-+$', '', newproduct.slug)

    newproduct.price=request.POST.get('productprice')
    newproduct.sellingprice=0

    category_name=request.POST.get('categoryselected')
    
    category_nameused=Category.objects.get(id=category_name)
    newproduct.category_name=category_nameused
    newproduct.desciption=request.POST.get('productdescription')
    newproduct.stock=request.POST.get('stock')
    newproduct.is_available=False
    subcategory_name=request.POST.get('subcategoryselected')
    subcategory_name1=request.POST.get('subcatogoryused')
    
    if int(newproduct.stock)>0:
        newproduct.is_available=True
    else:
        newproduct.is_available=False 

    if Subcategory.objects.filter(id=subcategory_name):
        subcategory_nameused=Subcategory.objects.get(id=subcategory_name)
        newproduct.subcategory_name=subcategory_nameused
    
    if 'productimage' in request.FILES: 
        newproduct.images=request.FILES["productimage"]
    else:
        messages.info(request,"Require all fields")
        
    newproduct.save()
    images=request.FILES.getlist('productimages')
    
    prodct=Products.objects.get(product_name=productname)
    

    for i in images:
        imageproduct=additionalimage()
        imageproduct.product=prodct
        imageproduct.images=i
        imageproduct.save()

    return redirect('adminproduct')

def modifythisproduct(request,pk):
    newproduct=Products.objects.get(id=pk)
    
    newproduct.product_name=request.POST.get('productname')
    newproduct.slug=request.POST.get('productname')

    newproduct.slug = newproduct.slug.lower().strip()
    newproduct.slug = re.sub(r'[^\w\s-]', '', newproduct.slug)
    newproduct.slug = re.sub(r'[\s_-]+', '-', newproduct.slug)
    newproduct.slug = re.sub(r'^-+|-+$', '', newproduct.slug)

    newproduct.price=request.POST.get('productprice')
    newproduct.sellingprice=0
    category_name=request.POST.get('categoryselected')
    
    
    category_nameused=Category.objects.get(id=category_name)
    newproduct.category_name=category_nameused
    newproduct.desciption=request.POST.get('productdescription')
    newproduct.stock=request.POST.get('stock')
    newproduct.is_available=False
    
    subcategory_name=request.POST.get('subcategoryselected')
    print(subcategory_name)
    if int(newproduct.stock)>0:
        newproduct.is_available=True
    else:
        newproduct.is_available=False 

    if Subcategory.objects.filter(subcategory_name=subcategory_name):
        subcategory_nameused=Subcategory.objects.get(subcategory_name=subcategory_name)
        newproduct.subcategory_name=subcategory_nameused
    
    if 'productimage' in request.FILES: 
        newproduct.images=request.FILES["productimage"]

    newproduct.save()
    if 'productimages' in request.FILES:
        images=request.FILES.getlist('productimages')

        for i in images:
            imageproduct=additionalimage()
            imageproduct.product=newproduct
            imageproduct.images=i
            imageproduct.save()

    else:
        messages.info(request,"Require all fields")
    
    return redirect('adminproduct')


def deleteproduct(request,pk):
    get_data=Products.objects.get(id=pk)
    get_data.delete()
    return redirect('adminproduct')

def modifyproduct(request,pk):
    print('modify')
    get_data=Products.objects.get(id=pk)

    otherimage=None
    if additionalimage.objects.filter(product=get_data).exists():
        otherimage=additionalimage.objects.filter(product=get_data)
    categories=Category.objects.all()
    context={"product":get_data,"categories":categories,"otherimage":otherimage}
    return render(request,'modifyproduct.html',context)

def load_subcategory(request):
    category_id=request.GET.get('categoryselected')
    subcategories=Subcategory.objects.filter(category_id)

def applyfilter(request):
    print("applyfitler")
    minval= request.POST.get('minvalue')

    maxvalue=request.POST.get('maxvalue')
    print(minval)
    print(maxvalue)
    listofproduct=Products.objects.filter(sellingprice__gte = minval).filter(sellingprice__lte =maxvalue)
    productcount=listofproduct.count
    context={'listofproducts':listofproduct,'productcount':productcount}
    return render(request,'userside/home.html',context)


@login_required(login_url='login')
def home(request,category_slug=None):
    print("I am at home")
    if request.user.is_authenticated and request.user.is_staff == True: 
        categories=None

        if category_slug==None:
            
            
            listofproduct= Products.objects.all()
            productcount=listofproduct.count
            print("heree")
            paginator=Paginator(listofproduct,9)
            page=request.GET.get('page')
            pagedproduct=paginator.get_page(page)
            context={'listofproducts':pagedproduct,'productcount':productcount}
            return render(request,'userside/home.html',context)
        
        else:
            categories=get_object_or_404(Category,slug=category_slug)
            listofproduct= Products.objects.filter(category_name=categories)
            print("hereeHy")
            productcount=listofproduct.count
            paginator=Paginator(listofproduct,9)
            page=request.GET.get('page')
            pagedproduct=paginator.get_page(page)
            context={'listofproducts':pagedproduct,'productcount':productcount}
            return render(request,'userside/home.html',context)
    else:
        return redirect("landingpage")


def myprofile(request):
    user=request.user
    name= request.user.username
    usernameid=Accounts.objects.get(username=name)
    x=str(usernameid.phone_number)
    x=x[-4:]
    
    code= name+x
    print(code)

    userx=usernameid.id
    referel=Referrel.objects.get(user=user)
    wallet=Wallet.objects.get(user=user)
    w=wallet.amount
    p=referel.code
    alladdressofuser=Address.objects.filter(username_id=usernameid)
    context={'user':user,'alladdressofuser':alladdressofuser,'referrel':p,'amount':w}
    return render(request,'userside/Yourprofile.html',context)

def myorders(request):
    userid=request.user
    print(userid)
    allorders=Orders.objects.filter(user=userid).order_by('-date')
    
    context={'allorders':allorders}
    return render(request,'userside/myorders.html',context)
 
def search(request):
    print("search")
    products=None
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Products.objects.order_by('-created_date').filter(Q(desciption__icontains=keyword)|Q(product_name=keyword)|Q(subcategory_name__subcategory_name=keyword))
    print(products)
    context={'listofproducts':products}
    return render (request,'userside/home.html',context)

@never_cache
def productshome(request,category_slug,product_slug):
    categories     =get_object_or_404(Category,slug=category_slug)
    addedtocart1=None
    productsdetails=get_object_or_404(Products,slug=product_slug)
    name= request.user 
    listofproduct= Products.objects.get(category_name=categories,product_name=productsdetails)
    additionalimages=additionalimage.objects.filter(product=listofproduct)
    if request.user.is_authenticated and request.user.is_admin==False:
        userpresent='yes'
        if Cart.objects.filter(product_id=listofproduct,username_id=name).exists():
            addedtocart1='yes'
            print('added to cart')
    context={'listofproducts':listofproduct,'addedtocart':addedtocart1,'additionalimages':additionalimages}
    
    return render(request,'userside/product-detail.html',context)


def addcart(request,pid):
    
    if request.user.is_authenticated == False:        
        request.session['productid']=pid
        #print(pid)
        return redirect('login')      
   
    
    name= request.user.username
    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    
    new_cartitem=Cart()
    product=Products.objects.get(id=pid)
    new_cartitem.product_id=product
    new_cartitem.totalquantity+=1
    new_cartitem.username_id=usernameid
    
    new_cartitem.save()
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    context={'allcart':allcart}
    return redirect('cart')

@login_required(login_url='login')
def cart(request):
    if request.user.is_admin==False:
        name= request.user.username
        count=0
        usernameid=Accounts.objects.get(username=name)
        userx=usernameid.id
        allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
        allcartproduct=Cart.objects.filter(username_id=usernameid.id)
        
        for eachcartproduct in allcartproduct:
            count=count+eachcartproduct.totalquantity
        
        context={'allcart':allcart}
        return render(request,'userside/cart.html',context)
    else:
        return redirect('login')

######################### PLACED ORDER #####################
def placedorder(request):
    addresss=request.POST['addressx']
    print(addresss)
    print("i am at placed order")
    name= request.user.username

    if Wallet.objects.filter(user=request.user).exists():
        existingwallet=Wallet.objects.get(user=request.user)
        existingwallet.amount=0
        existingwallet.save()

    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    addressofuser=Address.objects.get(username_id=usernameid,housename=addresss)
    alltotoffer=totalofferforuser.objects.filter(user=request.user)
    
    for i in allcart:
        updateproduct=Products.objects.get(id=i.product_id.id)
        
        updateproduct.stock=updateproduct.stock-i.totalquantity
        updateproduct.save()

        neworder=Orders()
        neworder.product=i.product_id
        neworder.quantity=i.totalquantity
        neworder.status="Placed"
        neworder.user=i.username_id
        neworder.Address=addressofuser
        
        w=0
        if alltotoffer is not None:
            w=0 
            for b in alltotoffer:
                w=b.totaloffer
            
            if i.product_id.sellingprice==0 or i.product_id.sellingprice==i.product_id.price:
                neworder.price =i.product_id.price*(neworder.quantity)-w
            else :
                neworder.price=(i.product_id.sellingprice)*(neworder.quantity)-w
        else:
            if i.product_id.sellingprice==0 or i.product_id.sellingprice==i.product_id.price:
                neworder.price =i.product_id.price*(neworder.quantity)-w
            else :
                neworder.price=i.product_id.sellingprice*(neworder.quantity)-w

        
        i.delete()
        print("neworder price " , neworder.price)
        neworder.save()

    
    
    for i in alltotoffer:
        i.delete()

    return JsonResponse({'status':True})
    return redirect('home')


############################ CHECK OUT ##########################
def deleteoffer(request):
    offerid=request.POST['offerid']
    print("pfferid ",offerid)
    offer=RealOffers.objects.get(id=offerid)
    offer.delete()
    print("deleted")
    return JsonResponse({'status':True})


def checkout(request):
    print("at checkout")
    name= request.user.username
    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    alladdressofuser=Address.objects.filter(username_id=usernameid)
    context={'allcart':allcart,'alladdressofuser':alladdressofuser}
    return render(request,'userside/place-order.html',context)  


def addaddress(request):
    newaddress=Address()
    newaddress.country=request.POST.get('country')
    newaddress.state=request.POST.get('state')
    newaddress.street=request.POST.get('street')
    newaddress.building_number=request.POST.get('building_number')
    newaddress.housename=request.POST.get('house_name')
    newaddress.pincode=request.POST.get('pincode')
    name= request.user.username
    newaddress.username_id=Accounts.objects.get(username=name)
    newaddress.save()
    return redirect('checkout')
def minus(request,productid):
    name= request.user.username

    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    print("minus worked")
    fetchcart=Cart.objects.get(product_id=productid,username_id=userx)
    fetchcart.totalquantity=fetchcart.totalquantity-1
    if fetchcart.totalquantity==0:
        print("deleted")
        fetchcart.delete()
    else:
        fetchcart.save()
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    context={'allcart':allcart}
    return redirect('cart')
    
def add(request):
    name= request.user.username
    totalamount=0
    productid=request.POST['prid']
    product_qty=request.POST['product_qty']
    print(productid)
    print("KKKKKKKKKK")
    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    productids=Products.objects.get(id=productid)
    fetchcart=Cart.objects.get(product_id=productids,username_id=userx)
    fetchcart.totalquantity=fetchcart.totalquantity+1
    fetchcart.save()
    print("addsaved")
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
   
    context={'allcart':allcart}
    return JsonResponse({'status':True})

def cancelorder(request):
    
    orderid=request.POST['orderid']
    which=request.POST['returnn']
    print("ehichh")
    print(which)
    if which=='cancel':
        orderupdate=Orders.objects.get(id=orderid)

        orderupdate.status="Cancelled"
        orderupdate.save()
        prod=Products.objects.get(id=orderupdate.product.id)
        prod.stock=prod.stock+1
        prod.save()
        print("pwolichh")

    else:
        orderupdate=Orders.objects.get(id=orderid)
        orderupdate.status="Picking up today"
        orderupdate.save()
    
    
    return JsonResponse({'status':True})


def add1(request):
    name= request.user.username
    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    productid=request.POST['productid']
    fetchcart=Cart.objects.get(product_id=productid,username_id=userx)

    totalquantity=request.POST['totquantity']
    print(totalquantity)
    fetchcart.totalquantity=totalquantity

    fetchcart.save()
    return JsonResponse({'status':True})
    productids=Products.objects.get(id=productid)

def checkcoupon(request):
    if request.user.is_admin==False:
        cartitems=Cart.objects.filter(username_id=request.user)
        
    code=request.POST['code']

    alloffers = Offers.objects.all()
    totoffer=0
    list=[]
    

    for i in alloffers:
        for j in cartitems:
            if i.code==code and i.category == j.product_id.category_name:
                totoffer=totoffer+j.product_id.price*i.offerpercentage/100
                x=i
                list.append(j)

            elif i.code==code and i.subcategory == j.product_id.subcategory_name:
                totoffer=totoffer+j.product_id.price*i.offerpercentage/100
                x=i
                list.append(j)

            elif i.code==code and i.product == j.product_id:
                totoffer=totoffer+j.product_id.price*i.offerpercentage/100
                x=i
                list.append(j)

    if totoffer != 0:
        for eachcart in list:
            gotoffer=UserObtainedOffer1()
            gotoffer.offer=x
            gotoffer.offerpricereduced=eachcart.product_id.price*x.offerpercentage/100
            gotoffer.cart=eachcart
            gotoffer.save()
            round(totoffer,2)

        totofferobj=totalofferforuser()
        if totoffer > 5000:
            totoffer=5000

        totofferobj.totaloffer=totoffer
        totofferobj.user=request.user
        totofferobj.save()
        print('xhechkout sucess')
        return JsonResponse({'status':True,'totoffer_price':totoffer})
    else:
        return JsonResponse({'status':False})
    
def removefromcart(request,productid):
    name= request.user.id
    print(name)
    usernameid=Accounts.objects.get(id=name)
    userx=usernameid.id
    fetchcart=Cart.objects.filter(product_id=productid).filter(username_id=name)
    fetchcart.delete()
    alltotoffer=totalofferforuser.objects.filter(user=request.user)
    for i in alltotoffer:
        i.delete()
    
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    context={'allcart':allcart}
    return redirect('cart')


from django.db.models import Count,Sum
from datetime import date

def dashboard(request):
    dweek=Orders.objects.values('date__week').annotate(sales=Count('id')).order_by('-date__week')
    for i in dweek:
        print(i)


    name= request.user.username
    
    dd=Orders.objects.values('date__date').annotate(sales=Count('id')).filter(status="Delivered").order_by('date__date')

    ddS=Orders.objects.values('date__date').annotate(sales=Count('id')).filter(status="Delivered").order_by('-date__date')[:2]
    
    ddmonthsales=Orders.objects.values('date__month').annotate(sales=Count('id')).filter(status="Delivered").order_by('date__month')
    ddmonthrev=Orders.objects.values('date__month').annotate(tot=Sum('product__price')).filter(status="Delivered").order_by('date__month')
    ddyear=Orders.objects.values('date__year').annotate(sales=Count('id')).filter(status="Delivered")
    drev=Orders.objects.values('date__date').annotate(tot=Sum('price')).filter(status="Delivered").order_by('date__date')
    #print(ddmonthrev)
    today = date.today()
    
    totalrev=0
    totalsales=0
    todaysales=0
    todayrevenue=0
    
    for i in dd:
        totalsales=totalsales+i['sales']
        if today== i['date__date']:
            todaysales= i['sales']
    for i in drev:
        totalrev=totalrev+i['tot']
        if today== i['date__date']:
            todayrevenue=i['tot']
    print("yessss")
    
    context={'name':name,'dd':dd,'drev':drev,'totalrev':totalrev,'totalsales':totalsales,'todaysales':todaysales,'todayrevenue':todayrevenue,'monthrev':ddmonthrev,'yearrev':ddyear}
    return render(request,'admindashboard.html',context)

from .utils import render_to_pdf
def revenuepdf(request):
    rowrev=Orders.objects.values('date__date').filter(status="Delivered").annotate(tot=Sum('price')).order_by('date__date')
    
    #print("$$$$$$$$$$$$$$$$$$$$")
    pdf = render_to_pdf('revenuereport.html', {'rowrev':rowrev})
    if pdf:
        response= HttpResponse(pdf,content_type='application/pdf')
        filename="Revenue_report%s.pdf"
        content="Inline;filename='%s'"%(filename)
        
        content="attachment; filename='%s'" %(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("Not found")
from datetime import datetime
def downloadreport(request):
    
    fromm=request.POST.get("from")
    frommm = datetime.strptime(fromm, '%Y-%m-%d')
    
    print(fromm)
    to  = request.POST.get("to")
    too = datetime.strptime(to, '%Y-%m-%d')
    
    
    rad=request.POST.get('dd')
    dweek=Orders.objects.values('date__week').filter(date__range=(fromm,to)).filter(status="Delivered").annotate(sales=Count('id')).order_by('-date__week')
    print(dweek)

    if rad == "pdf":
        return salespdf(frommm,too)
    else:
        return salesexcel(fromm,to)


import time
def salespdf(fromm,to):

    dd=Orders.objects.all().filter(date__range=(fromm,to)).filter(status="Delivered")
    
    pdf = render_to_pdf('salesreport.html', {'rowrev':dd})
    
    if pdf:
        response= HttpResponse(pdf,content_type='application/pdf')
        filename="Sales_report%s.pdf"
        content="Inline;filename='%s'"%(filename)
        
        content="attachment; filename='%s'" %(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("Not found")

def salesexcel(fromm,to):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sales_Report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['User', 'Product','Qty' ,'Address', 'MRP' ,'Selling Price', 'Total Price','Order Status']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    #dd=Orders.objects.values_list('user__username').annotate(sales=Count('id')).order_by('date__date')
    dd=Orders.objects.values_list('user__username','product__product_name','quantity','Address__housename','product__price','product__sellingprice','price','status').filter(status="Delivered").filter(date__range=(fromm,to))
        
    for row in dd:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

def downloadreceipt(request,pk):
    order=Orders.objects.get(id=pk)
    pdf = render_to_pdf('invoice.html', {'order':order})
    if pdf:
        response= HttpResponse(pdf,content_type='application/pdf')
        filename="Invoice%s.pdf"
        content="Inline;fiename='%s'"%(filename)
        
        content="attachment; filename='%s'" %(filename)
        response['Content-Disposition']=content
        return response




def downloadrevexcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Revenue_Report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'Revenue' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rowrev=Orders.objects.values_list('date__date').annotate(tot=Sum('price')).order_by('date')
    rows = Accounts.objects.all().values_list('username','first_name', 'last_name', 'email')
    
    
    for row in rowrev:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

def adminoffersReal(request):
    newoffers=RealOffers.objects.all()
    print(newoffers)
    context={'alloffers':newoffers}
    return render(request,'adminoffersReal.html',context)


def adminoffers(request):
    newoffers=Offers.objects.all()
    context={'alloffers':newoffers}
    return render(request,'adminoffers.html',context)

def addoffersReal(request):
    
    return render(request,'addofferReal.html')

def salesReport(request):
    key1=Orders.objects.filter().order_by('-date__date')
    
    return render(request,'adminsalesReport.html',{'key1':key1})

def addoffers(request):
    return render(request,'addoffer.html')

def minval(request,minval):
    print(minval)
    return render(request,'userside/minval.html')

def addthiscoupon(request):
    code=request.POST.get('code')
    price=request.POST.get('price')
    item=request.POST.get('item')
    item2=request.POST.get('item2')
    newoffer=Offers()           #This is foor COUPON ONLY 
    if item == "category":
        catoffer=Category.objects.get(slug=item2)
        newoffer.category=catoffer

    elif item == "subcategory":
        subcat=Subcategory.objects.get(slug=item2)
        newoffer.subcategory=subcat
    
    else:
        product=Products.objects.get(slug=item2)
        newoffer.product=product
    
    newoffer.code=code
    newoffer.offerpercentage=price
    newoffer.save()

    return redirect('adminoffers')


def addthisoffer(request):        ##For Real Offer##
    offername=request.POST.get('code')
    price=request.POST.get('price')
    item=request.POST.get('item')
    item2=request.POST.get('item2')
    newoffer=RealOffers()
    if item == "category":
        catoffer=Category.objects.get(slug=item2)
        newoffer.category=catoffer

    elif item == "subcategory":
        subcat=Subcategory.objects.get(slug=item2)
        newoffer.subcategory=subcat
        
    else:
        product=Products.objects.get(slug=item2)
        newoffer.product=product
    
    newoffer.offername=offername
    newoffer.offerpercentage=price
    newoffer.save()

    return redirect('adminoffersReal')