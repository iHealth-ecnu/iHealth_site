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

### TODO
* [x] 【接口】获取文章首页列表
* [x] 【接口】获取文章详情
* [x] 【接口】用户登陆验证
* [x] 【接口】模糊匹配指定用户名，返回符合的用户列表
* [x] 【接口】获取用户详情
* [x] 【接口】用户注册
* [x] 【接口】根据 id 批量请求用户信息
* [x] 【接口】点赞数更新
* [x] 【接口】个性化推荐文章
* [ ] 【接口】获取用户个人病历
* [ ] 【接口】获取某用户的主治医生信息

### 接口说明
API 接口采用 RESTful 规范设计

什么是 RESTful 请看：[怎样用通俗的语言解释REST，以及RESTful？ - 知乎](https://www.zhihu.com/question/28557115)


----
* 获取首页文章列表

示例：http://ihealth.yangyingming.com/api/v1/articlelist?page=1&limit=10&userID=5a02e30be6c80c1c9ecdaea7

请求方式：GET

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------       |
| page     | 1        | 取第几页的数据  |
| limit    | 10       | 一次取多少个    |
| userID   | None     | 用户ID,个性化推荐用 |

----

* 获取文章详情

示例：http://ihealth.yangyingming.com/api/v1/articledetail?id=59ec737bdfdeee3708bc5d0f

请求方式：GET

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| id       | None     | 取指定id的文章详情 |

----

* 用户登陆验证

示例：http://ihealth.yangyingming.com/api/v1/usercheck

请求方式：POST

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| email       | None     | 待验证用户的邮箱 |
| password       | None     | 待验证用户的密码 |

----
* 模糊匹配指定用户名，返回符合的用户列表

示例：http://ihealth.yangyingming.com/api/v1/userlist?name=小明

请求方式：GET

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| name       | ''     | 模糊匹配条件 |
| selfname       | ''     | 需要排除的name值 |
| limit       | 10     | 最多匹配多少条结果 |

----

* 获取用户详情

示例：http://ihealth.yangyingming.com/api/v1/user?id=59fb1595dfdeee2b4c26c346

请求方式：GET

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| id       | None     | 用户id |

----

* 用户注册

示例：http://ihealth.yangyingming.com/api/v1/reguser

请求方式：POST

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| email       | None     | 注册邮箱 |
| password       | None     | 密码 |
| nickname       | None     | 用户昵称 |
| name       | None     |用户真实姓名 |
| sex       | None     | 性别 0:女 1:男|
| usertype       | None     | 用户类别 0:游客 1:患者 2:医生 3:管理员 |
| birthday       | None     | 用户出生日期 |
| introduction       | None     | 个人介绍 |
| age       | None     | 用户年龄 |
| phone       | None     | 注册手机号 |

----

* 根据ID批量获取用户信息

示例：http://ihealth.yangyingming.com/api/v1/userlistbyid?id=59fb1595dfdeee2b4c26c347,59fb1595dfdeee2b4c26c348

请求方式：GET

| 参数      | 默认值   | 说明 |
| -------- | -------- | --------          |
| id       | None     | 要获取的用户id，可以是多个 |

----

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

### 参考资料
* client 提交post 到 django出现403错误  
  http://blog.csdn.net/watsy/article/details/9009847
