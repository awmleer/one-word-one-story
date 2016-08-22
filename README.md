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


## 版本升级中的部署操作步骤
1. 关掉`setting.py`中的`DEBUG`
2. 把本地项目上传至服务器
3. 关闭uwsgi进程 `uwsgi --stop /tmp/{{ 你在uwsgi.ini中设置的名字 }}.pid`
4. 数据库 `python manage.py makemigrations`和`python manage.py migrate`
5. 静态文件收集 `python manage.py collectstatic`
6. 启动uwsgi `uwsgi --ini uwsgi.ini`
7. 注：如果你不需要进行45这两步操作，你也可以直接通过`uwsgi --reload /tmp/{{ 你在uwsgi.ini中设置的名字 }}.pid`来重启uwsgi

## 其他
- 初始化项目请先在控制台执行`python manage.py makemigrations`和`python manage.py migrate`
- 此外还需要在根目录下新建一个文件夹`Media`，里面放上一张图片`avatar_default.png`作为默认的用户头像