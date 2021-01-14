from django.test import TestCase
from mainapp.models import Product, ProductCategory, ProductType


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(name="Tables")
        type = ProductType.objects.create(name="Comfort")
        self.product_1 = Product.objects.create(name="Table black",
                                                category=category,
                                                type=type,
                                                price=199,
                                                quantity=150)

        self.product_2 = Product.objects.create(name="Table white",
                                                category=category,
                                                type=type,
                                                price=299,
                                                quantity=125,
                                                is_active=False)

        self.product_3 = Product.objects.create(name="Table gray",
                                                category=category,
                                                type=type,
                                                price=399,
                                                quantity=115)

    def test_product_get(self):
        product_1 = Product.objects.get(name="Table black")
        product_2 = Product.objects.get(name="Table white")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Product.objects.get(name="Table black")
        product_2 = Product.objects.get(name="Table white")
        type = ProductType.objects.get(name='Comfort')
        self.assertEqual(str(product_1), 'Table black (Tables)')
        self.assertEqual(str(product_2), 'Table white (Tables)')
        self.assertEqual(str(type), 'Comfort')

    def test_product_get_items(self):
        product_1 = Product.objects.get(name="Table black")
        product_3 = Product.objects.get(name="Table gray")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
