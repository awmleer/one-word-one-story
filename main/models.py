from django.db import models

class Person(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='person')
    name = models.CharField(max_length=50, default='新用户')
    avatar=models.FileField(upload_to='avatars')
    introduction= models.CharField(max_length=100, default='暂无个人介绍')
    phone = models.CharField(max_length=20, blank=True, default='')
    last_modified_time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class Story(models.Model):
    first_word=models.CharField(max_length=500, default='')
    create_user=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stories_created')
    words=models.ManyToManyField('Word',related_name='story')
    def __str__(self):
        return self.first_word

class Word(models.Model):
    text=models.CharField(max_length=50, default='')
    user=models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stories_participated')
    def __str__(self):
        return self.text
