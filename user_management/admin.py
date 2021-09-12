from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Settings, User, Info, Review

# Register your models here.
# admin.site.register(User, UserAdmin)
admin.site.register(User)
admin.site.register(Info)
admin.site.register(Review)
admin.site.register(Settings)
