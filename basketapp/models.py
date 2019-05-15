from django.db import models
from django.conf import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super().delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.user.username + ' ' + self.product.name

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete()

    @staticmethod
    def get_item(self, pk):
        return Basket.objects.filter(pk=pk).first()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - Basket.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)


