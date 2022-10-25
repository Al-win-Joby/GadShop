from . import views

from django.urls import path

urlpatterns = [
     path('',views.categories,name="categories"),
     path('add-category',views.addcat,name="addcategory"),
     path('addthiscategory',views.addthiscat,name="addthiscategory"),
     path('addthissubcategory',views.addthissubcategory,name="addthissubcategory"),
     path('addsubcategory',views.addsubcategory,name="addsubcategory"),
     path('deletecategory/<int:pk>',views.deletecategory,name="deletecategory"),
     path('modifycategory/<int:pk>',views.modifycategory,name="modifycategory"),
     path('modifythiscategory/<int:pk>',views.modifythiscategory,name="modifythiscategory"),
     path('subcategories',views.subcategories,name="subcategories")
     
]
