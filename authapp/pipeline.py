from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    # print(response.keys())
    if backend.name == 'vk-oauth2':
        api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                    access_token=response['access_token'],
                                                    v='5.92')), None))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]

        if 'about' in data and data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        # if 'photo' in response.keys():
        #     user.avatar = response['photo']

        if 'about' in data and data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if 'bdate' in data and data['bdate']:
                bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
                user.age = timezone.now().date().year - bdate.year
        user.save()

    elif backend.name == 'google-oauth2':
        # print(response.keys())
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'email' in response.keys():
            user.email = response['email']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 14:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')
        user.save()

    return
