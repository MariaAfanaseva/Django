from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver


def get_activation_key_time():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    # class Meta:
    #     verbose_name = 'Пользователь'
    #     verbose_name_plural = 'Пользователи'  # for admin

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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, on_delete=models.CASCADE)
    tags = models.CharField(verbose_name='Tags', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='About You', max_length=512, blank=True)
    gender = models.CharField(verbose_name='Gender', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)  # create form
        else:
            instance.shopuserprofile.save()  # save form
