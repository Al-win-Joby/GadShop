
from django.urls import path
from . import views
urlpatterns = [
     path('adminproduct',views.adminproduct,name="adminproduct"),
     path('addproduct',views.addproduct,name="addproduct"),
     path('subcataddproduct/<int:catid>',views.subcataddproduct,name="subcataddproduct"),
     path('selectitem/<str:x>',views.selectitem,name='selectitem'),
     path('addthisproduct',views.addthisproduct,name='addthisproduct'),
     path('modifythisproduct/<int:pk>',views.modifythisproduct,name='modifythisproduct'),
     path('load-subcategory/',views.load_subcategory,name="ajax_load_subcategory"),
     path('deleteproduct/<int:pk>',views.deleteproduct,name="deleteproduct"),
     path('modifyproduct/<int:pk>',views.modifyproduct,name="modifyproduct"),
     path('home',views.home,name="home"),
     path('applyfilter',views.applyfilter,name="applyfilter"),     
     path('checkout',views.checkout,name="checkout"),
     path('cart',views.cart,name="cart"),
     path('salesexcel',views.salesexcel,name="salesexcel"),
     path('downloadrevexcel',views.downloadrevexcel,name="downloadrevexcel"),
     path('dashboard',views.dashboard,name="dashboard"),
     path('adminoffers',views.adminoffers,name="adminoffers"),
     path('adminoffersReal',views.adminoffersReal,name="adminoffersReal"),
     path('maxvalue/<int:minval>',views.minval,name="minval"),

     path('addthiscoupon',views.addthiscoupon,name="addthiscoupon"),
     path('addthisoffer',views.addthisoffer,name="addthisoffer"),
     path('addoffers',views.addoffers,name="addoffers"),
     path('salesReport',views.salesReport,name="salesReport"),
     
     path('addoffersReal',views.addoffersReal,name="addoffersReal"),
     path('minus/<int:productid>',views.minus,name="minus"),
     path('removefromcart/<int:productid>',views.removefromcart,name="removefromcart"),
     path('addaddress',views.addaddress,name="addaddress"),
     
     path('deleteoffer',views.deleteoffer,name="deleteoffer"),
     
     path('placedorder',views.placedorder,name="placedorder"),
     path('add',views.add,name="add"),
     path('cancelorder',views.cancelorder,name="cancelorder"),
     path('add1',views.add1,name="add1"),
     path('checkcoupon',views.checkcoupon,name="checkcoupon"),
     path('downloadreport',views.downloadreport,name="downloadreport"),
     path('addcart/<int:pid>',views.addcart,name="addcart"),
     path('myorders',views.myorders,name="myorders"),  

     path('myprofile',views.myprofile,name="myprofile"),
     path('search',views.search,name="search"),
     path('revenuepdf',views.revenuepdf,name="revenuepdf"),

     path('salespdf',views.salespdf,name="salespdf"),
     path('downloadreceipt/<int:pk>',views.downloadreceipt,name="downloadreceipt"),

     path('categories/<slug:category_slug>',views.home,name="filteredhome"),
     path('categories/<slug:category_slug>/<slug:product_slug>',views.productshome,name="showproduct"),
     path('categoriess',views.productshome,name="showproducts"),
       
     
]
  