from django.contrib import admin

# Register your models here.

from apps.users.models import UserProfile

#自定义UserProfileAdmin注册
# class UserProfileAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(UserProfile,UserProfileAdmin)

#利用UserAdmin优化
#导入UserAdmin
from django.contrib.auth.admin import UserAdmin
admin.site.register(UserProfile,UserAdmin)