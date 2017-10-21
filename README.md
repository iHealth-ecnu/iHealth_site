## iHealth-site
iHealth 项目的后台程序

### Django 搭建笔记
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