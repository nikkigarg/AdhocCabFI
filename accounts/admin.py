from django.contrib import admin

# Register your models here.
from accounts.models import User
from django.contrib.auth.models import ContentType, Permission

admin.site.register(ContentType)
admin.site.register(Permission)
admin.site.register(User)