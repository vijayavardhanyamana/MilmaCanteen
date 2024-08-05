from django.contrib import admin

from service.models import login

class login_l(admin.ModelAdmin):
    list_display=('name','email','password')

admin.site.register(login,login_l)