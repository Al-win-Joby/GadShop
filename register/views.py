import email
from itertools import product
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.http import JsonResponse
from account.models import Accounts, Orders ,Referrel ,Wallet
from django.urls import reverse
import os
from store import views as pp
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from twilio.rest import Client

from store.models import Products, RealOffers
# Create your views here.
def loginn(request):
    if request.user.is_authenticated:
        
      if request.user.is_admin==False:
         return redirect('store/home')
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')
global rotp
global user 
def signedup(request):
    if request.method=='POST':
        #print("signedup")
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('first_name')
        referrel= request.POST.get('referrel')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        phone_number=request.POST.get('phone_number')
        if email=="" or first_name=="" or last_name=="" or username=="" or password1=="" or password2=="" or phone_number=="":
            messages.info(request,"Require all fields")
            return render(request,'signup.html')
        if password1==password2: 
            if Accounts.objects.filter(username=username).exists():
                messages.info(request,"User exist")
                
                return render(request,'signup.html')
            elif Accounts.objects.filter(email=email).exists():
                messages.info(request,"Email exist")
                
                return render(request,'signup.html')
            else:
                global referrelG 
                referrelG=""
                if referrel != "":
                    if Referrel.objects.filter(code=referrel).exists():
                        referrelG = referrel


                global user 
                
                user={'first_name':first_name,'last_name':last_name,'phone_number':phone_number,'username':username,'email':email,'password':password1}
                #user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
                
                
                return redirect('signed_up')

        else:
             return render(request,'signup.html')


def signed_up(request):
    global rotp
    rotp=getotp()
    #print("user created but not saved")
    global user
    
    return render(request,'otp.html')

def verifynumber(request):
    global rotp
    global user
    phone_number=request.POST.get('phone_number')
    #print(phone_number+"dddddddddd")
    if Accounts.objects.filter(phone_number=phone_number).exists():
        user=Accounts.objects.get(phone_number=phone_number)
        print(user.username)
        if user is not None:
            
            rotp=getotp()
    else:
        messages.info(request,"Invalid number")
        return render(request,'forgotpassword.html')
    
    return render(request,'otplogin.html')

def verifylogin(request):
    if request.method=='POST':
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        number=first+second+third+fourth
        global rotp
        
        if(number==str(rotp)):
            #print("correct")
            global user
            if user is not None:
               
                login(request,user)
                return redirect('home')
            
            else:
                messages.info(request,"Invalid number")
       
                return render(request,'otplogin.html')

        return render(request,'otplogin.html')
    return render(request,'otplogin.html')

def verify(request):
    if request.method=='POST':
        first=request.POST.get('first')
        second=request.POST.get('second')
        third=request.POST.get('third')
        fourth=request.POST.get('fourth')
        number=first+second+third+fourth
        global rotp
        
        if(number==str(rotp)):
            #print("correct")
            global referrelG
            global user
            if user is not None:
                
                
                
               
                first_name=user["first_name"]
                last_name=user["last_name"]
                phone_number=user["phone_number"]
                username=user["username"]
                email=user["email"]
                password1=user["password"]
                user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
                
                wallet=Wallet()
                wallet.user=user
                wallet.save()

                referrel=Referrel()
                referrel.user=user
                x=str(phone_number)
                x=x[-4:]
                
                code = first_name+x
                referrel.code=code
                
                referrel.save()


                if referrelG != "":
                    if Referrel.objects.filter(code=referrelG).exists():
                        referlobj=Referrel.objects.get(code=referrelG)
                        walletuser=referlobj.user
                        #if Wallet.objects.filter(user=walletuser).exists():
                        existingwallet=Wallet.objects.get(user=walletuser)
                        existingwallet.amount=existingwallet.amount+50
                        existingwallet.save()

                return redirect('home')
         
        else:
            #print('thettipoi')
            messages.info(request,"Incorrect OTP")
            return render(request,'otp.html')

    return redirect('/')

def getotp():
    import random

    # prints a random value from the list
    
    list=range(1000,9999)
    otp=random.choice(list)
    

    account_sid ='AC55ee27ce60089f5fb5d3dedca4e23b0f'
    auth_token = '06f3dca6c18adcf6cf8543a937638bdc'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    body = otp,
    from_ = '+13252214515',
    to    = '+919746701683' 
    )
    print("otp poytind")
    return otp
    #print(message.sid)

def forgotpassword(request):
    return render(request,'forgotpassword.html')

def loggedin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is None: 
            
            messages.info(request,"Invalid credentials")
        elif user is not None:
            
            if user.is_staff==True:
                login(request,user)
                
                if 'productid' in request.session:
                    prod=Products.objects.get(id=int(request.session['productid']))
                    
                    
                    return pp.productshome(request,prod.category_name.slug,prod.slug)

                    
                return redirect('home')
            else:
                messages.info(request,"Blocked by admin")
    return render(request,'login.html') 

def landingpage(request):
    if request.user.is_authenticated:
        
      if request.user.is_admin==False:
         return redirect('store/home')
    
    listofproduct= Products.objects.all()
    context={'listofproducts':listofproduct}
    return render(request,'index.html',context)
from django.db.models import Q
def searchG(request):
    keyword= request.GET['search']
    listofproduct=Products.objects.order_by('-created_date').filter(Q(desciption__icontains=keyword)|Q(product_name=keyword)|Q(subcategory_name__subcategory_name=keyword))

    context={'listofproducts':listofproduct}
    return render(request,'index.html',context)
    
def statusupdate(request):
    orderid=request.POST['orderid']
    statusx=request.POST['statusvalue']
    
    
    order=Orders.objects.get(id=orderid)
    if statusx== "Returned" :
        prod=Products.objects.get(id=order.product.id)
        prod.stock=prod.stock+1
        prod.save()
        

    order=Orders.objects.get(id=orderid)
    order.status=statusx
    order.save()
    return JsonResponse({'status':True})

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated and request.user.is_staff == True: 

        # if 'productid' in request.session:
        #     x=request.session['productid']
        #     print("home ethi  ",x)
        #     prod=Products.objects.get(id=int(x))
            

        listofproduct= Products.objects.all()
        offer=RealOffers.objects.all()
        productcount=listofproduct.count #9
        
        paginator=Paginator(listofproduct,9)
        page=request.GET.get('page')
        pagedproduct=paginator.get_page(page)
        
        
        for i in listofproduct:    
            i.afteroffer
            
        context={'listofproducts':pagedproduct,'productcount':productcount,"inoffer":offer}
        return render(request,'userside/home.html',context)
    else:
        return redirect("landingpage")

def orderdetails(request):
    allorders=Orders.objects.all().order_by('-date')
    name= request.user.username
    context={'allorders':allorders,'name':name}
    return render(request,'adminorders.html',context)

def adminlogin(request):
    if request.user.is_authenticated:
      if request.user.is_admin==True:
        
        return redirect('adminhome')
      else:
        
        return render(request,'adminlogin.html')
    return render(request,'adminlogin.html')

def adminloggedin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is not None:

            if user.is_admin==True:
                
                login(request,user)
                return redirect('adminhome')
        else:
            messages.info(request,"Invalid Credentials")
            
    return render(request,'adminlogin.html') 

def logout1(request):
    logout(request)
    return redirect("landingpage")

@login_required(login_url='login')
def  adminhome(request):
    if request.user.is_admin==False:
         return redirect("login")

    name= request.user.username
    key1=Accounts.objects.all().order_by('id')
    context={'name':name,'key1':key1}
    return render(request,'adminhome.html',context)

@login_required(login_url='login')
def createadminuser(request):
    name= request.user.username
    return render(request,'createadmin.html',{'name':name})

@login_required(login_url='login')
def addadminuser(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2') 
        if email=="" or first_name=="" or last_name=="" or username=="" or password1=="" or password2=="" or phone_number=="":
            messages.info(request,"Require all fields")
            return render(request,'createadmin.html')
        if password1==password2: 
            if Accounts.objects.filter(username=username).exists():
                messages.info(request,"User exist")
               
                name= request.user.username
                return render(request,'createadmin.html',{'name':name})

            elif Accounts.objects.filter(email=email).exists():
                messages.info(request,"Email exist")
                name= request.user.username
                return render(request,'createadmin.html',{'name':name})
            else:
                user= Accounts.objects.create_superuser(first_name=first_name,last_name=last_name,phone_number=phone_number,username=username,email=email,password=password1)
        return redirect('adminhome')
    
    else:
        return redirect('adminhome')

def edit1(request,pk):
   get_data=Accounts.objects.get(id=pk)
   if get_data.is_staff == True:
    get_data.is_staff=False
    get_data.save()
   else:
    get_data.is_staff=True
    get_data.save()
   return redirect(adminhome)

def delete(request,pk):
    get_data=Accounts.objects.get(id=pk)
    get_data.delete()
    return redirect(adminhome)
