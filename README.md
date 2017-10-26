## iHealth-site
iHealth 项目的后台程序

### 依赖
* Django==1.8.17
* pymongo==3.4.0
* uWSGI==2.0.15

### 启动项目
1. 本地启动（windows）：
```
python manage.py runserver 0.0.0.0:8000
```

2. 打开浏览器访问 **http://127.0.0.1:8000/**  
  出现 **Hello, I am iHealth ' backend!** 表示启动成功

3. 测试其它接口  
获取文章列表：http://127.0.0.1:8000/api/v1/articlelist  
获取文章详情：http://127.0.0.1:8000/api/v1/articledetail?id=59ec737bdfdeee3708bc5d0f

### 接口说明
API 接口采用 RESTful 规范设计

什么是 RESTful 请看：[怎样用通俗的语言解释REST，以及RESTful？ - 知乎](https://www.zhihu.com/question/28557115)


* 获取首页文章列表

**http://ihealth.yangyingming.com/api/v1/articlelist**

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------       |
| page     | 1        | 取第几页的数据  |
| limit    | 10       | 一次取多少个    |

示例：http://ihealth.yangyingming.com/api/v1/articlelist?page=1&limit=5

* 获取文章详情

**http://ihealth.yangyingming.com/api/v1/articledetail?id=59ec737bdfdeee3708bc5d0f**

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| id       | None     | 取指定id的文章详情 |

示例：http://ihealth.yangyingming.com/api/v1/articledetail?id=59ec737bdfdeee3708bc5d0f


### Django 搭建笔记（笔记部分，和项目无关）
1. 创建项目目录
```
django-admin startproject iHealth_site
```

2. 运行自带服务器进行测试
```
python manage.py runserver 0.0.0.0:8000
```
**注意**：想要外网访问需要在 settings.py 的 ALLOWED_HOSTS = ['\*']

3. 创建app目录
```
python manage.py startapp mysite
```

### MongoDB 配置
1. 开启 MongoDB 权限认证：**在配置文件中加入 auth = true**

2. 创建管理员用户（如果你是第一次使用 MongoDB）  
```
use admin
db.createUser({user:"admin",pwd:"admin123",roles:["userAdminAnyDatabase"]})
```
管理员用户用来创建其他数据库和用户

3. 使用管理员账户远程登录
```
C:\Users\cs>mongo [your_ip]:27017
> use admin
switched to db admin
> db.auth('admin','admin123')
1
```

4. 创建 iHealth 数据库，以及操作该数据库的用户
```
use iHealth         // 创建 iHealth 数据库，并作为认证数据库
db.createUser({
    user:'admin',   // 用户名
    pwd:'admin123', // 用户密码
    roles:[{role:'readWrite',db:'iHealth'}]     // 为该用户赋予数据库的读写权限
})
```

5. 使用该用户远程登录 iHealth 数据库
```
C:\Users\cs>mongo [your_ip]:27017
> use iHealth
switched to db iHealth
> db.auth('admin','admin123')
1
> db.getCollectionNames()
[ ]
```
数据库刚刚创建，所以没有数据