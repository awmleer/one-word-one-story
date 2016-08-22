from django.db import models
from django.utils import timezone


class Person(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='person')
    name = models.CharField(max_length=50, default='新用户')
    avatar=models.ImageField(upload_to='avatars',default='avatar_default.png')
    introduction= models.CharField(max_length=100, default='暂无个人介绍')
    phone = models.CharField(max_length=20, blank=True, default='')
    stars=models.PositiveIntegerField(default=0)
    points=models.PositiveIntegerField(default=0)
    last_reply_story = models.DateTimeField(auto_now_add=True)
    last_create_story = models.DateTimeField(auto_now_add=True)
    # last_modified_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Story(models.Model):
    first_word=models.TextField(max_length=500, default='')
    create_user=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stories')
    publish_time=models.DateTimeField(auto_now_add=True)
    last_reply_time=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.first_word


class Word(models.Model):
    text=models.TextField(max_length=500, default='')
    story=models.ForeignKey('Story',related_name='words')
    publish_time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='words')
    like_users=models.ManyToManyField('auth.User',related_name='like_words')
    def __str__(self):
        return self.text


# todo 点赞