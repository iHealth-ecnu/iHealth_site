#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from models import *
import sys
import json
from django.views.decorators.csrf import csrf_exempt
import hashlib



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


    #未登录用户
    if userID == None:
        # 获取数据
        article_list = Articles().find_all()
    else:
        #获取用户对应的labels
        labels = Users().find_label(userID)
        if labels == {} or labels == None:
            #用户没有labels
            article_list = Articles().find_all()
            if labels == None: #对没有labels的用户设置labels
                Users().insert_label(userID)
        else:
            # 获取对应label的数据
            article_list = Articles().find_labelArticle(labels)

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
        if id == None:
            return HttpResponse('请提供 id 参数!')
        # 更新文章阅读量
        Articles().updateRead(id=id,cnt=1)
        # 获取数据
        article = Articles().find_one(id=id)
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
    try:
        id=request.GET.get('id',None)
        if id == None:
            return HttpResponse('请提供 id 参数!')

        Articles().updateUpvote(id=id)
        res = {
            'msg' : '点赞成功！',
            'result' : True,
        }
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
        elif MD5(user['password']) == real_user['password']:
            real_user['_id'] = str(real_user['_id'])
            del real_user['password']
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
        limit = int(request.GET.get('limit',10))
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
        data['password'] = MD5(data['password'])
        #设初始labels为空，个性化推荐用
        data['labels'] = {}
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

def changeNickname(request):
    try:
        userID = request.GET.get('id',None)
        name = request.GET.get('newName',None)
        if userID==None or name==None:
            raise Exception,'注册信息参数不完整'

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

def changePhone(request):
    try:
        userID = request.GET.get('id',None)
        Phone = request.GET.get('newPhone',None)
        if userID==None or Phone==None:
            raise Exception,'注册信息参数不完整'

        Users().changePhone(userID,Phone)
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