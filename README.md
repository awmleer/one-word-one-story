# 一人一句话
一个人一句话，组成一个奇妙的故事。


##环境配置说明
centos 6+  
nginx  
python 3.5.2  
django 1.10  
pytz  
Pillow 3.3.1
uwsgi

## 其他
- 初始化项目请先在控制台执行`python manage.py makemigrations`和`python manage.py migrate`
- 此外还需要在根目录下新建一个文件夹`Media`，里面放上一张图片`avatar_default.png`作为默认的用户头像