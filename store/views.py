from ast import keyword
from multiprocessing import context
from sre_constants import SUCCESS
from unicodedata import category
from django.shortcuts import render,redirect
from django.contrib import messages
from account.models import Accounts, Address,Orders
from cart.models import Cart
from store.models import Products, additionalimage
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

def deleteproduct(request,pk):
    get_data=Products.objects.get(id=pk)
    get_data.delete()
    return redirect('adminproduct')

def load_subcategory(request):
    category_id=request.GET.get('categoryselected')
    subcategories=Subcategory.objects.filter(category_id)

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
    userx=usernameid.id
    alladdressofuser=Address.objects.filter(username_id=usernameid)
    context={'user':user,'alladdressofuser':alladdressofuser}
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
            products=Products.objects.order_by('-created_date').filter(Q(desciption__icontains=keyword)|Q(product_name=keyword))
    print(products)
    context={'listofproducts':products}
    return render (request,'userside/home.html',context)

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

@login_required(login_url='login')
def addcart(request,pid):

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
    usernameid=Accounts.objects.get(username=name)
    userx=usernameid.id
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    addressofuser=Address.objects.get(username_id=usernameid,housename=addresss)
    for i in allcart:
        updateproduct=Products.objects.get(id=i.product_id.id)
        print("stock ")
        updateproduct.stock=updateproduct.stock-i.totalquantity
        updateproduct.save()
        
        neworder=Orders()
        neworder.product=i.product_id
        neworder.quantity=i.totalquantity
        neworder.status="Placed"
        neworder.user=i.username_id
        neworder.Address=addressofuser
        
        i.delete()
        neworder.save()        
    return JsonResponse({'status':True})
    return redirect('home')


############################ CHECK OUT ##########################
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


def removefromcart(request,productid):
    name= request.user.id
    print(name)
    usernameid=Accounts.objects.get(id=name)
    userx=usernameid.id
    fetchcart=Cart.objects.filter(product_id=productid).filter(username_id=name)
    fetchcart.delete()
    allcart=Cart.objects.filter(username_id=userx).filter(totalquantity__gt = 0).order_by('id')
    context={'allcart':allcart}
    return render(request,'userside/cart.html',context)


from django.db.models import Count,Sum
from datetime import date

def dashboard(request):
    name= request.user.username
    orders=Orders.objects.all
    daily=Orders.objects.filter(date__range=["2022-10-01", "2022-11-01"])
    dd=Orders.objects.values('date__date').annotate(sales=Count('id')).order_by('date__date')

    ddS=Orders.objects.values('date__date').annotate(sales=Count('id')).order_by('-date__date')[:2]
    
    ddmonthsales=Orders.objects.values('date__month').annotate(sales=Count('id')).order_by('date__month')
    ddmonthrev=Orders.objects.values('date__month').annotate(tot=Sum('product__price')).order_by('date__month')
    ddyear=Orders.objects.values('date__year').annotate(sales=Count('id'))
    drev=Orders.objects.values('date__date').annotate(tot=Sum('product__price')).order_by('date__date')
    print(drev)
    today = date.today()
    print(ddmonthrev)
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