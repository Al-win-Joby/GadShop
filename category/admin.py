from django.contrib import admin
from category.models import Category, Subcategory
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')

class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('subcategory_name',)}
    list_display=('category_name','slug')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory,SubcategoryAdmin)