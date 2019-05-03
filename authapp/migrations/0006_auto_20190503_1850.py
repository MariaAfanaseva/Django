# Generated by Django 2.1.7 on 2019-05-03 16:50

import authapp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_auto_20190428_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivation',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('activation_key', models.CharField(blank=True, max_length=128)),
                ('activation_key_expires', models.DateTimeField(default=authapp.models.get_activation_key_time)),
            ],
        ),
        migrations.RemoveField(
            model_name='shopuser',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='shopuser',
            name='activation_key_expires',
        ),
    ]
