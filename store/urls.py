
from django.urls import path
from . import views
urlpatterns = [
     path('adminproduct',views.adminproduct,name="adminproduct"),
     path('addproduct',views.addproduct,name="addproduct"),
     path('subcataddproduct/<int:catid>',views.subcataddproduct,name="subcataddproduct"),
     path('addthisproduct',views.addthisproduct,name='addthisproduct'),
     path('load-subcategory/',views.load_subcategory,name="ajax_load_subcategory"),
     path('deleteproduct/<int:pk>',views.deleteproduct,name="deleteproduct"),
     path('home',views.home,name="home"),
     path('checkout',views.checkout,name="checkout"),
     path('cart',views.cart,name="cart"),
     path('dashboard',views.dashboard,name="dashboard"),
     
     path('minus/<int:productid>',views.minus,name="minus"),
     path('removefromcart/<int:productid>',views.removefromcart,name="removefromcart"),
     path('addaddress',views.addaddress,name="addaddress"),
     
     path('placedorder',views.placedorder,name="placedorder"),
     path('add',views.add,name="add"),
     path('add1',views.add1,name="add1"),
     path('addcart/<int:pid>',views.addcart,name="addcart"),
     path('myorders',views.myorders,name="myorders"),  

     path('myprofile',views.myprofile,name="myprofile"),
     path('search',views.search,name="search"),

     path('categories/<slug:category_slug>',views.home,name="filteredhome"),
     path('categories/<slug:category_slug>/<slug:product_slug>',views.productshome,name="showproduct"),
       
     
]
  