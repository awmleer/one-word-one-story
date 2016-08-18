from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate #用户登录认证
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
        res=HttpResponse('success', content_type="text/plain")
    return res
