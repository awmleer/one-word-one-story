from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^index/',views.index,name='index'),
]