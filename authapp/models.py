from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


def get_activation_key_time():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='age', null=True)
    is_active = models.BooleanField(verbose_name='Active', default=True)
    email = models.EmailField(verbose_name='Email', unique=True)


class UserActivation(models.Model):
    user = models.OneToOneField(ShopUser, on_delete=models.CASCADE, primary_key=True)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=get_activation_key_time)

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
