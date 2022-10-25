from multiprocessing import context
from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from category.models import Category,Subcategory
import re
# Create your views here.
@login_required(login_url='login')
def categories(request):
    name= request.user.username
    key1=Category.objects.all()
    context={'name':name,'key1':key1}
    return render(request,'admincategory.html',context)

@login_required(login_url='login')
def addcat(request):                                   
    name= request.user.username         
    return render (request,'addcategory.html',{'name':name})

@login_required(login_url='login')
def addthiscat(request):
    newcategory=Category()
    newcategory.category_name=request.POST.get("catname")
    newcategory.slug=request.POST.get("catname")
    categoryname=request.POST.get("catname")
    if Category.objects.filter(category_name=categoryname):
        messages.info(request,"Category exists")
        return render(request,'addcategory.html')
    newcategory.slug = newcategory.slug.lower().strip()
    newcategory.slug = re.sub(r'[^\w\s-]', '', newcategory.slug)
    newcategory.slug = re.sub(r'[\s_-]+', '-', newcategory.slug)
    newcategory.slug = re.sub(r'^-+|-+$', '', newcategory.slug)

    newcategory.description=request.POST.get("catdescription")
    #print(len(request.FILES['image']))
    if 'categoryimage' in request.FILES: 
        newcategory.category_image=request.FILES["categoryimage"]
    else :
        messages.info(request,"Require all fields")
        return render(request,'addcategory.html')
    newcategory.save()    
   
    return redirect('categories')

def addsubcategory(request):
    name= request.user.username   
    categories=Category.objects.all()   
    return render(request,'addsubcategory.html',{'name':name,'categories':categories})

def addthissubcategory(request):
    newsubcategory=Subcategory()
    newsubcategory.subcategory_name=request.POST.get("subcategoryname")
    subcatname=request.POST.get("subcategoryname")
    if Category.objects.filter(subcategory_name=subcatname):
        messages.info(request,"Subcategory exists")
        return render(request,'addsubcategory.html') 
    category_name=request.POST.get("categoryselected")
    category_selected=Category.objects.get(id=category_name)
    newsubcategory.category_name=category_selected
    newsubcategory.slug=request.POST.get("subcategoryname")

    newsubcategory.slug = newsubcategory.slug.lower().strip()
    newsubcategory.slug = re.sub(r'[^\w\s-]', '', newsubcategory.slug)
    newsubcategory.slug = re.sub(r'[\s_-]+', '-', newsubcategory.slug)
    newsubcategory.slug = re.sub(r'^-+|-+$', '', newsubcategory.slug)
    newsubcategory.save()
    return redirect('subcategories')



@login_required(login_url='login')
def deletecategory(request,pk):
    get_data=Category.objects.get(id=pk)
    get_data.delete()
    return redirect('categories')

@login_required(login_url='login')

def modifycategory(request,pk):
    get_data=Category.objects.get(id=pk)
    name= request.user.username
    pk              =get_data.id 
    print(pk)
    categoryname    =get_data.category_name
    description     =get_data.description
    categoryimage   =get_data.category_image
    
    context={'key1':get_data,'description':description,'categoryname':categoryname}
    return render (request,'modifycategory.html',context)

@login_required(login_url='login')
def modifythiscategory(request,pk):
    upadte_data=Category.objects.get(id=pk)
    upadte_data.category_name=request.POST.get("catname") 
    upadte_data.slug=request.POST.get("catname")

    upadte_data.slug = upadte_data.slug.lower().strip()
    upadte_data.slug = re.sub(r'[^\w\s-]', '', upadte_data.slug)
    upadte_data.slug = re.sub(r'[\s_-]+', '-', upadte_data.slug)
    upadte_data.slug = re.sub(r'^-+|-+$', '', upadte_data.slug)
    print(upadte_data.slug)
    upadte_data.description=request.POST.get("catdescription")
    if 'categoryimage' in request.FILES:
        upadte_data.category_image=request.FILES["categoryimage"]
    # else :
    #     #upadte_data.category_image=request.FILES["categoryimage"]
    #     #messages.info(request,"Require all fields")
    #     context={'key1':upadte_data}
    #     return render (request,'modifycategory.html',context)
    upadte_data.save()
    return redirect('categories')    

def subcategories(request):
    name= request.user.username
    key1=Subcategory.objects.all()
    context={'name':name,'key1':key1}
    return render(request,'adminsubcategory.html',context)
    