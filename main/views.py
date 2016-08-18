from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,AnonymousUser
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

def user_identify(request):
    context={}
    if isinstance(request.user,AnonymousUser):
        context['has_logged_in']=False
    else:
        context['has_logged_in']=True
        context['user']={'name':request.user.person.name}
    return context



def index(request):
    context=user_identify(request)
    return render(request,'index.html',context)



def story_add(request):
    context = user_identify(request)
    return render(request,'story_add.html',context)