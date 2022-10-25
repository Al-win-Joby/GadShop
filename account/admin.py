from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Accounts

# Register your models here.
class AccountAdmin(UserAdmin):
    list_display=('first_name','email','username','last_login','date_joined','is_admin')
    filter_horizontal=()
    list_filter=()
    field_sets=()
admin.site.register(Accounts,AccountAdmin)