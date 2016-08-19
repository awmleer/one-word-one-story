from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^index/$',views.index,name='index'),
    url(r'^story/add/$',views.story_add,name='story_add'),
    url(r'^story/(?P<story_id>[0-9]+)/$',views.story_detail,name='story_detail'),
    url(r'^story/(?P<story_id>[0-9]+)/reply/$',views.story_reply,name='story_reply'),
    url(r'^about/$', views.about, name='about'),
    url(r'^me/$', views.me_setting, name='me'), #默认进入的是“个人设置”
    url(r'^me/created/$', views.me_created, name='me_created'),
    url(r'^me/participated/$', views.me_participated, name='me_participated'),
    url(r'^me/setting/$', views.me_setting, name='me_setting'),
    url(r'^me/modify/$', views.me_modify, name='me_modify'),
    url(r'^me/changepwd/$', views.me_changepwd, name='me_changepwd'),
    url(r'^me/avatar/$', views.me_avatar, name='me_avatar'),
]