# Generated by Django 2.1.7 on 2019-04-15 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20190415_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='hot_product',
            field=models.BooleanField(default=False, verbose_name='акция'),
        ),
    ]
