# encoding: utf8

from django.contrib.auth import login, authenticate
from django.http import  HttpResponseRedirect
from django.shortcuts import render

from duoshuo import DuoshuoAPI

from django.conf import settings
from .models import UserProfile
from .models import User

import random


def callback(request):
    code = request.GET.get('code')
    direct = request.GET.get('from', '/')

    ds = DuoshuoAPI(
        short_name=settings.DUOSHUO_SHORT_NAME, 
        secret=settings.DUOSHUO_SECRET
    )

    response = ds.get_token(code)
    uid = response["user_id"]

    if UserProfile.objects.filter(duoshuo_id=uid).exists():
        profile = UserProfile.objects.get(duoshuo_id=uid)
        profile.user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, profile.user)
    else:
        response = ds.users.profile(user_id=response["user_id"])
        if response["code"] != 0:
            return 

        ds_user = response["response"]

        password = ''.join([
            random.choice('abcdefg&#%^*f') \
                    for i in range(8)]
            )

        _unique_name = ds_user["name"]
        while User.objects.filter(username=_unique_name).count():
            _unique_name = _unique_name + str(random.randrange(1,100))

        user =  User.objects.create_user(
                username=_unique_name, 
                email='user@example.com', 
                password=password
            )
        
        userprofile = UserProfile(
                user=user, 
                duoshuo_id=ds_user['user_id'], 
                username=ds_user["name"], 
                avatar=ds_user['avatar_url']
            )
        userprofile.save()

        user = authenticate(
                username=_unique_name, 
                password=password
            )

        login(request, user)

    return HttpResponseRedirect('/')
