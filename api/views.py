#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from models import *
import sys
import json
from django.views.decorators.csrf import csrf_exempt
import hashlib
import random


def MD5(s):
    '''对字符串s进行md5加密，并返回'''
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def hello(request):
    '''测试接口'''
    return HttpResponse("Hello, I am iHealth ' backend!")

def articleList(request):
    '''文章接口'''
    # 提取参数
    page = int(request.GET.get('page',1))
    limit = int(request.GET.get('limit',10))
    userID = request.GET.get('userID', None)
    #cate为首页显示的的文章分类，None时返回所有文章
    cate = request.GET.get('cate', None)

    #文章分类为空时：
    if cate == None:
        # 获取数据
        article_list = Articles().find_all()
    else:
        #文章分类为 推荐
        if cate == 'recommend':
            #游客，返回所有文章
            if userID == None:
                article_list = Articles().find_all()
            else:
                #返回用户label
                labels = Users().find_label(userID)
                if labels == {} or labels == None:
                    #用户没有labels
                    article_list = Articles().find_all()
                    if labels == None:
                        #对没有labels的用户设置labels
                        Users().insert_label(userID)
                else:
                    # 获取对应label的数据
                    # article_C每一维为一个分类的文章
                    article_C = Articles().find_recommendArticle(labels)
                    # num_arc_beg 起始文章标号 num_arc_end 结束文章标号
                    num_arc_beg = (page - 1) *  limit
                    num_arc_end = page * limit
                    article_list = []
                    len_c = len(article_C)
                    for i in range(num_arc_beg, num_arc_end):
                        article_list.append(article_C[i%len_c][i/len_c])
                    #一页的文章随机打乱
                    # random.shuffle(article_list)
                    #直接返回
                    res_list = []
                    for article in article_list:
                        # 将对象中不是字符串的变量值转换为字符串
                        article['_id'] = article['_id'].__str__()
                        article['pubdate'] = article['pubdate'].__str__()
                        # article['content'] = article['content'].strip()
                        article['intro'] = article['intro'].strip()
                        del article['content']
                        res_list.append(article)
                    # 转换为JSON
                    # res = json.dumps(res_list, indent=4, ensure_ascii=False, encoding='utf-8')
                    res = json.dumps(res_list, indent=4)
                    return HttpResponse(res, content_type='application/json')
        else:
            article_list = Articles().find_labelArticle(cate)

    # 截取数据
    article_list = article_list[(page-1)*limit:(page-1)*limit+limit]
    res_list = []
    for article in article_list:
        # 将对象中不是字符串的变量值转换为字符串
        article['_id'] = article['_id'].__str__()
        article['pubdate'] = article['pubdate'].__str__()
        # article['content'] = article['content'].strip()
        article['intro'] = article['intro'].strip()
        del article['content']
        res_list.append(article)
    # 转换为JSON
    # res = json.dumps(res_list, indent=4, ensure_ascii=False, encoding='utf-8')
    res = json.dumps(res_list, indent=4)
    return HttpResponse(res, content_type='application/json')

def articleDetail(request):
    '''文章详情接口'''
    try:
        # 提取参数
        id = request.GET.get('id',None)
        userID = request.GET.get('userID', None)

        if id == None:
            return HttpResponse('请提供 id 参数!')
        # 更新文章阅读量
        Articles().updateRead(id=id,cnt=1)
        # 获取数据
        article = Articles().find_one(id=id)
        # 更新用户label，个性化推荐用 阅读暂定+1
        if userID != None:
            Users().update_label(userID, article['category'], 1)
        # 准备文章数据，转换为 JSON
        del article['_id']
        del article['intro']
        article['pubdate'] = article['pubdate'].__str__()
        article['content'] = article['content'].strip()
        res = json.dumps(article, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'msg' : '文章详情获取失败！',
            'reason' : str(e),
        }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')

def doUpvote(request):
    '''点赞接口'''
    try:
        id=request.GET.get('id',None)
        userID = request.GET.get('userID', None)
        if id == None:
            return HttpResponse('请提供 id 参数!')

        Articles().updateUpvote(id=id)
        res = {
            'msg' : '点赞成功！',
            'result' : True,
        }
        article = Articles().find_one(id=id)
        # 更新用户label，个性化推荐用 点赞暂定+10
        if userID != None:
            Users().update_label(userID, article['category'], 10)
    except Exception,e:
        res = {
            'msg' : '点赞失败！',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res, indent=4)
    return HttpResponse(res, content_type='application/json')

# 添加该装饰器以关闭默认post提交的csrf验证
@csrf_exempt
def userCheck(request):
    '''检查用户是否可以登录'''
    try:
        # 获取post提交的数据
        user = request.POST
        print user
        real_user = Users().find_one_by_email(user['email'])
        if real_user == None:
            res = {
                'msg' : '用户登陆验证未通过！',
                'reason' : 'User is not found.',
                'result' : False,
            }
        elif user['password'] == real_user['password']:     #取消MD5再次加密
            real_user['_id'] = str(real_user['_id'])
            # del real_user['password']
            res = {
                'msg' : '用户登陆验证通过！',
                'data' : real_user,
                'result' : True,
            }
        else:
            res = {
                'msg' : '用户登陆验证未通过！',
                'reason' : 'Password error.',
                'result' : False,
            }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'msg' : '用户登陆验证过程失败！',
            'reason' : str(e),
            'result' : False,
        }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')


def userList(request):
    '''获取用户列表'''
    try:
        # 提取参数
        name = request.GET.get('name','')
        selfname = request.GET.get('selfname','')
        limit = int(request.GET.get('limit',25))
        # 获取数据
        user_list = Users().find_many_by_name(name)
        # 截取数据
        user_list = user_list[:limit]
        res_list = []
        for user in user_list:
            # 将对象中不是字符串的变量值转换为字符串
            user['_id'] = user['_id'].__str__()
            # 排除掉自身
            if user['name']==selfname:
                continue
            del user['password']
            res_list.append(user)
        # 转换为JSON
        res = json.dumps(res_list, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'msg' : '模糊匹配失败指定用户名失败！',
            'reason' : str(e),
        }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')


def userDetail(request):
    '''用户详情接口'''
    try:
        # 提取参数
        id = request.GET.get('id',None)
        if id == None:
            return HttpResponse('请提供 id 参数!')
        # 获取数据
        user = Users().find_one(id=id)
        #出于安全性，将password字段去掉
        del user['password']
        # 准备文章数据，转换为 JSON
        user['_id'] = str(user['_id'])
        res = json.dumps(user, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'msg' : '用户详情获取失败！',
            'reason' : str(e),
        }
    res = json.dumps(res, indent=4)
    return HttpResponse(res, content_type='application/json')

@csrf_exempt
def regUser(request):
    '''注册用户'''
    try:
        data = request.POST.copy()
        print data
        # 判断是否已存在该邮箱注册的账号
        if not (data.has_key('email') and data.has_key('password') and data.has_key('nickname') and data.has_key('sex') and data.has_key('usertype') and data.has_key('birthday')):
            raise Exception,'注册信息参数不完整'
        if Users().find_one_by_email(data['email']) != None:
            raise Exception,'邮箱已被注册过'
        # 插入数据
        #将下面一行注释掉，取消MD5再次加密
        #data['password'] = MD5(data['password'])
        #设初始labels为空，个性化推荐用
        data['labels'] = {}
        
        #初始化用户病历字段
        data['medicalRecord']=[]
        data['age'] = int(data['age'])
        data['sex'] = int(data['sex'])
        data['usertype'] = int(data['usertype'])
        
        Users().insert_one(data)
        res = {
            'msg' : '用户注册成功！',
            'result' : True,
        }
    except Exception,e:
        res = {
            'msg' : '用户注册失败！',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res, indent=4)
    return HttpResponse(res, content_type='application/json')

def test(request):
    return render(request,'index.html')


#根据id，进行密码验证
def check_password(id,password):
    realPwd = Users().get_password_by_id(id)
    if password == realPwd:
        return True
    else :
        return False

#根据id列表取出users用于群聊
def userListByID(request):
    try:
        usersId=request.GET.get('id',None)
        if usersId == None:
            raise Exception,'请提供 id 参数'

        usersID=usersId.split(',')

        users=[]
        for ID in usersID:
            temp=Users().find_one(id=ID)
            temp['_id']=temp['_id'].__str__()
            users.append(temp)
        res = {
            'msg' : '获取成功！',
            'data' : users,
            'result' : True,
        }
    except Exception,e:
        res = {
            'msg' : '获取失败！',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res, indent=4)
    return HttpResponse(res, content_type='application/json')

#修改昵称
@csrf_exempt
def changeNickname(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('password') and data.has_key('newName')):
            raise Exception,'注册信息参数不完整'
        userID = data['id']
        password = data['password']
        name = data['newName']
        if check_password(userID,password) == False:
            res = {
                'msg' : '修改失败，请保证网络安全',
                'result' : False,
            }
        else :
            Users().changeNickname(userID,name)
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')

#修改手机号
@csrf_exempt
def changePhone(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('password') and data.has_key('newPhone')):
            raise Exception,'注册信息参数不完整'
        userID = data['id']
        password = data['password']
        phone = data['newPhone']
        if check_password(userID,password) == False:
            res = {
                'msg' : '修改失败，请保证网络安全',
                'result' : False,
            }
        else :
            Users().changePhone(userID,phone)
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')

#修改姓名
@csrf_exempt
def changeName(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('password') and data.has_key('newName')):
            raise Exception,'注册信息参数不完整'
        userID = data['id']
        password = data['password']
        name = data['newName']

        if check_password(userID,password) == False:
            res = {
                'msg' : '修改失败，请保证网络安全',
                'result' : False,
            }
        else :
            Users().changeName(userID,name)
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')


#修改性别
@csrf_exempt
def changeSex(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('password') and data.has_key('newSex')):
            raise Exception,'注册信息参数不完整'
        userID = data['id']
        password = data['password']
        sex = data['newSex']

        if check_password(userID,password) == False:
            res = {
                'msg' : '修改失败，请保证网络安全',
                'result' : False,
            }
        else :
            Users().changeSex(userID,sex)
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')

#修改密码，需要同时输入原密码和新密码
@csrf_exempt
def changePassword(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('oldPassword') and data.has_key('newPassword')):
            raise Exception,'注册信息参数不完整'
        userID = data['id']
        oldPwd = data['oldPassword']
        newPwd = data['newPassword']

        if check_password(userID,oldPwd) == False:   #取消MD5再次加密
            res = {
                'msg' : '密码错误，修改失败',
                'result' : False,
            }
        else :
            Users().changePassword(userID,newPwd)   #取消MD5再次加密
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')

#修改出生日期
@csrf_exempt
def changeBirthday(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('password') and data.has_key('newBirthday')):
            raise Exception,'注册信息参数不完整'
        print data
        userID = data['id']
        password = data['password']
        Date = data['newBirthday']

        if check_password(userID,password) == False:
            res = {
                'msg' : '修改失败，请保证网络安全',
                'result' : False,
            }
        else :
            Users().changeBirthday(userID,Date)
            res = {
                'msg' : '修改成功',
                'result' : True,
            }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')

#写入病历
@csrf_exempt
def addMedicalRecord(request):
    try:
        data = request.POST.copy()
        if not(data.has_key('id') and data.has_key('date') and data.has_key('doctor') and data.has_key('content')):
            raise Exception,'注册信息参数不完整'
        print data
        userID = data['id']

        toData = {}
        toData['date']=data['date']
        toData['doctor']=data['doctor']
        toData['content']=data['content']
        Users().addMedicalRecord(userID,toData)
        res = {
            'msg' : '修改成功',
            'result' : True,
        }
    except Exception,e:
        res={
            'msg' : '修改失败',
            'reason' : str(e),
            'result' : False,
        }
    res = json.dumps(res,indent=4)
    return HttpResponse(res, content_type='application/json')
