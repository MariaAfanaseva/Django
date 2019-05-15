from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Forming'),
        (SENT_TO_PROCEED, 'Sent to proceed'),
        (PAID, 'Paid'),
        (PROCEEDED, 'Proceeded'),
        (READY, 'Ready'),
        (CANCEL, 'Cancel'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order')
    created = models.DateTimeField(verbose_name='create', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='update', auto_now=True)
    status = models.CharField(verbose_name='status',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='active', default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Current order: {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.values_list('quantity', flat=True)
        return sum(items)

    def get_product_type_quantity(self):
        return self.orderitems.count()

    def get_total_cost(self):
        items = self.orderitems.select_related('product')
        return sum([el.quantity * el.product.price for el in items])

    # переопределяем метод, удаляющий объект
    def delete(self):
        for item in self.orderitems.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="orderitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
