from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User,AnonymousUser
from django.views.decorators.http import require_http_methods
import django.contrib.auth as auth #用户登录认证
from django.contrib.auth.decorators import login_required,permission_required
from main.models import *
import datetime
from django.utils import timezone
import json

import logging
from django.shortcuts import redirect

# Get an instance of a logger
logger = logging.getLogger('django')

def user_identify(request):
    return {
        'has_logged_in': not isinstance(request.user,AnonymousUser),
        'user':request.user
    }



@require_http_methods(["GET"])
def index(request):
    context=user_identify(request)
    context['stories']=Story.objects.order_by('-last_reply_time')[:30]
    return render(request,'index.html',context)



@login_required
@require_http_methods(["GET","POST"])
def story_add(request):
    if request.method=='GET': #GET请求
        context = user_identify(request)
        res=render(request,'story_add.html',context)
    else: #POST请求
        story=Story.objects.create(first_word=request.POST['first_word'],create_user=request.user)
        person=request.user.person
        person.last_create_story=timezone.now()
        person.points+=3
        person.save()
        data={
            'status':'success',
            'story_id':story.id
        }
        res=HttpResponse(json.dumps(data), content_type="application/json")
    return res



@require_http_methods(["GET"])
def story_detail(request,story_id):
    context = user_identify(request)
    story=Story.objects.get(id=story_id)
    context['story']=story
    context['words']=story.words.order_by('publish_time')
    return render(request,'story_detail.html',context)


@login_required
@require_http_methods(["POST"])
def story_reply(request,story_id):
    if request.POST['word']:
        story=Story.objects.get(id=story_id)
        story.last_reply_time=timezone.now()
        Word.objects.create(text=request.POST['word'],story=story,user=request.user)
        person=request.user.person
        person.last_reply_story=timezone.now()
        person.points += 2
        person.save()
        res=HttpResponse('success', content_type="text/plain")
    else:
        res=HttpResponse('fail', content_type="text/plain")
    return res


@login_required
@require_http_methods(["GET"])
def me_created(request):
    context = user_identify(request)
    context['stories']=request.user.stories.order_by('-publish_time')[:30]
    return render(request, 'me_created.html', context)


@login_required
@require_http_methods(["GET"])
def me_participated(request):
    context = user_identify(request)
    context['words']=request.user.words.order_by('-publish_time')[:30]
    return render(request, 'me_participated.html', context)


@login_required
@require_http_methods(["GET"])
def me_setting(request):
    context = user_identify(request)
    return render(request, 'me_setting.html', context)


@login_required
@require_http_methods(["GET","POST"])
def me_modify(request):
    if request.method=='GET':
        context = user_identify(request)
        return render(request, 'me_modify.html', context)
    else:
        if not request.POST['name']:
            return HttpResponse('请输入昵称', content_type="text/plain")
        person=request.user.person
        person.name=request.POST['name']
        request.user.email=request.POST['email']
        person.introduction=request.POST['introduction']
        person.save()
        request.user.save()
        return HttpResponse('success', content_type="text/plain")



@login_required
@require_http_methods(["GET","POST"])
def me_changepwd(request):
    if request.method=='GET':
        context = user_identify(request)
        return render(request, 'me_changepwd.html', context)
    else:
        if not request.POST['password_old']:
            return HttpResponse('请输入旧密码', content_type="text/plain")
        if not request.POST['password_new']:
            return HttpResponse('请输入新密码', content_type="text/plain")
        user= auth.authenticate(username=request.user.username, password=request.POST['password_old'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                # User is valid, active and authenticated
                user.set_password(request.POST['password_new'])
                user.save()
                auth.logout(request)
                return HttpResponse('success', content_type="text/plain")
            else:
                # The password is valid, but the account has been disabled!
                return HttpResponse('您的账号已被锁定', content_type="text/plain")
        else:
            # the authentication system was unable to verify the username and password
            # The username and password were incorrect.
            return HttpResponse('您输入的密码错误', content_type="text/plain")



@login_required
@require_http_methods(["POST"])
def me_avatar(request):
    context = user_identify(request)
    if request.FILES['avatar']:
        context['status'] = 'fail' #默认状态是fail
        logger.info(request.FILES['avatar'])
        if request.FILES['avatar'].size>204000:
            context['status'] = 'too_big'
        else:
            avatar = request.user.person.avatar
            logger.info(request.FILES['avatar'].size)
            # 如果原来的不是默认头像，就把旧头像先删掉
            if avatar.url != '/media/avatar_default.png':
                avatar.delete()  # 删除旧的头像
            avatar.save(request.user.username+'_'+request.FILES['avatar'].name, request.FILES['avatar'])
            context['status'] = 'success'

    return render(request, 'me_avatar.html', context)




@require_http_methods(["GET"])
def about(request):
    context = user_identify(request)
    return render(request, 'about.html', context)



@login_required
@require_http_methods(["GET"])
def like(request):
    if request.GET['type']=='like_word':
        word=Word.objects.get(id=request.GET['id'])
        word.like_users.add(request.user)
        # todo 自己不能给自己star
        person_who_word=word.user.person
        person_who_word.points += 5
        person_who_word.stars += 1
        person_who_word.save()
        return HttpResponse('success', content_type="text/plain")
    else:
        return HttpResponse('fail', content_type="text/plain")

