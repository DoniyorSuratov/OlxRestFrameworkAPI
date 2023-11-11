from django.contrib import admin

from main.models import Product, Category

# Register your models here.
admin.site.register((Product,Category))

