# Generated by Django 2.1.7 on 2019-05-06 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_shopuserprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='aboutMe',
            field=models.TextField(blank=True, max_length=512, verbose_name='About You'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('W', 'Female')], max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='tags',
            field=models.CharField(blank=True, max_length=128, verbose_name='Tags'),
        ),
    ]
