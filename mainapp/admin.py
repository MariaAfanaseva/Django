from django.contrib import admin
from .models import Product, ProductCategory


class ProductInline(admin.TabularInline):
    model = Product
    fields = 'name', 'short_desc', 'price',
    extra = 1


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    inlines = ProductInline,


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = 'name', 'category__name',
    list_display = 'name', 'category', 'quantity', 'price',
    list_filter = 'name',

