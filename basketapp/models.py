from django.db import models
from django.conf import settings
from mainapp.models import Product
from django.utils.functional import cached_property


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)
    add_datetime = models.DateTimeField(verbose_name='datetime add', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    # def get_total_quantity(self):
    #     _items = self.get_items_cached
    #     return sum(list(map(lambda x: x.quantity, _items)))
    #
    # def get_total_cost(self):
    #     _items = self.get_items_cached
    #     return sum(list(map(lambda x: x.product_cost, _items)))

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.user.username + ' ' + self.product.name

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

