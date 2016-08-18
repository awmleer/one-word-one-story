from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
import django.contrib.auth as auth #用户登录认证
from django.contrib.auth.decorators import login_required,permission_required
from main.models import *
import datetime
from django.utils import timezone

import logging
from django.shortcuts import redirect

# Get an instance of a logger
logger = logging.getLogger('django')


@require_http_methods(["GET","POST"])
def login(request):
    logger.info(request.method)
    # 如果是GET请求
    if request.method=='GET':
        context={}
        res=render(request, 'login.html', context)
    # 如果是POST请求
    else:
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                # User is valid, active and authenticated
                auth.login(request, user)
                res = HttpResponse('success', content_type="text/plain")
            else:
                # The password is valid, but the account has been disabled!
                res = HttpResponse('您的账号已被锁定', content_type="text/plain")
        else:
            # the authentication system was unable to verify the username and password
            # The username and password were incorrect.
            res = HttpResponse('用户名或密码错误', content_type="text/plain")
    return res


def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')