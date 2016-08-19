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



@require_http_methods(["GET","POST"])
def signup(request):
    # 如果是GET请求
    if request.method=='GET':
        context={}
        res=render(request, 'signup.html', context)
    # 如果是POST请求
    else:
        # 一些简单的表单验证
        if not request.POST['username']:
            return HttpResponse('请输入用户名', content_type="text/plain")
        if not request.POST['name']:
            return HttpResponse('请输入昵称', content_type="text/plain")
        if not request.POST['password']:
            return HttpResponse('请输入密码', content_type="text/plain")

        # 如果数据库中已经存在了这个用户名
        if len(User.objects.filter(username=request.POST['username'])) > 0:
            return HttpResponse('您输入的用户名已经被注册过了', content_type="text/plain")

        # 正常情况
        new_user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        if new_user is not None:
            # 创建info
            new_person = Person.objects.create(user=new_user,name=request.POST['name'])
            if request.POST['introduction']:
                new_person.introduction=request.POST['introduction']
            new_person.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)
            res = HttpResponse('success', content_type="text/plain")
        else:
            res = HttpResponse('注册失败', content_type="text/plain")
    return res


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')