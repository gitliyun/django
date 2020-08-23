from django.contrib import admin
from .models import UserInfo


# Register your models here.
# 修改django 内部认证表后，需要将自定义的表在admin.py中注册，否则admin后台不显示
admin.site.register(UserInfo)








