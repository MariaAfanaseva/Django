from django.db import models
from shop.storage_backends import MediaStorage


class ProductCategory(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(verbose_name='category name', max_length=128, unique=True)
    description = models.TextField(verbose_name='category description', blank=True)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    def __str__(self):
        return self.name


class ProductType(models.Model):

    name = models.CharField(verbose_name='type', max_length=128, unique=True)
    description = models.TextField(verbose_name='description type', blank=True)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='product name', max_length=128)
    image = models.ImageField(upload_to='products_images',storage=MediaStorage(),
                              blank=True)
    short_desc = models.CharField(verbose_name='product short description', max_length=60, blank=True)
    description = models.TextField(verbose_name='product description', blank=True)
    price = models.DecimalField(verbose_name='product price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='quantity in stock', default=0)
    is_active = models.BooleanField(verbose_name='active', default=True, db_index=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')
