from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^index/',views.index,name='index'),
    url(r'^story/add/',views.story_add,name='story_add'),
    url(r'^story/(?P<story_id>[0-9]+)/$',views.story_detail,name='story_detail'),
    url(r'^story/(?P<story_id>[0-9]+)/reply/$',views.story_reply,name='story_reply'),
]