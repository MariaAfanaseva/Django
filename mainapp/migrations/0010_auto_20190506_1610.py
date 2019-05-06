# Generated by Django 2.1.7 on 2019-05-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20190419_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='product description'),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=128, verbose_name='product name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='product price'),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='quantity in stock'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_desc',
            field=models.CharField(blank=True, max_length=60, verbose_name='product short description'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='category description'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='name',
            field=models.CharField(max_length=128, unique=True, verbose_name='category name'),
        ),
    ]