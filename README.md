## iHealth-site
iHealth 项目的后台程序

### Django 搭建笔记
* 创建项目目录
```
django-admin startproject iHealth_site
```

* 运行自带服务器进行测试
```
python manage.py runserver 0.0.0.0:8000
```
**注意**：想要外网访问需要在 settings.py 的 ALLOWED_HOSTS = ['\*']

* 创建app目录
```
python manage.py startapp mysite
```