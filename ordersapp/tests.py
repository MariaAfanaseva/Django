from django.test import TestCase
from ordersapp.models import Order, OrderItem
from authapp.models import ShopUser
from mainapp.models import Product, ProductType, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self):
        self.user = ShopUser.objects.create(username='Mari')
        category = ProductCategory.objects.create(name="Tables")
        type = ProductType.objects.create(name="Comfort")
        self.product_1 = Product.objects.create(name="Table black",
                                                category=category,
                                                type=type,
                                                price=199,
                                                quantity=150)
        self.order = Order.objects.create(user=self.user)
        self.products_order = OrderItem.objects.create(order=self.order,
                                                       product=self.product_1,
                                                       quantity=15)

    def test_order_get(self):
        products_order = OrderItem.objects.get(order=self.order)
        self.assertEqual(products_order, self.products_order)

    def test_order_str(self):
        order = Order.objects.get(user=self.user)
        self.assertEqual(str(order), 'Current order: ' + str(order.id))
