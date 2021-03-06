from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product, ProductType
from django.contrib.auth.models import User
from authapp.models import ShopUser

import json
import os

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        types = load_from_json('types')

        ProductType.objects.all().delete()
        for type in types:
            new_type = ProductType(**type)
            new_type.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category

            type_name = product["type"]
            _type = ProductType.objects.get(name=type_name)
            product['type'] = _type

            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.create_superuser('admin', 'admin@admin.com', 'admin')
