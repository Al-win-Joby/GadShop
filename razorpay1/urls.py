from . import views

from django.urls import path

urlpatterns = [
     path('razorpay',views.razorpay1,name="razorpay"),
     
]
