from django.contrib import admin

# Register your models here.
from .models import Food, FoodCategory


# 分别注册模型

admin.site.register(Food)
admin.site.register(FoodCategory)

