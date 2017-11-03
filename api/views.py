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
    # 获取数据
    article_list = Articles().find_all()
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
            'info' : '文章详情获取失败！',
            'reason' : str(e)
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
        real_user = Users().find_one_by_email(user['email'])
        if real_user == None:
            res = {
                'info' : '用户登陆验证未通过！原因：用户不存在！',
                'reason' : False
            }
        elif MD5(user['password']) == real_user['password']:
            real_user['_id'] = str(real_user['_id'])
            del real_user['password']
            res = {
                'info' : '用户登陆验证通过！',
                'reason' : True,
                'data' : real_user
            }
        else:
            res = {
                'info' : '用户登陆验证未通过！原因：密码错误！',
                'reason' : False
            }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'info' : '用户登陆验证过程失败！',
            'reason' : str(e)
        }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')


def userList(request):
    '''获取用户列表'''
    try:
        # 提取参数
        name = request.GET.get('name','')
        limit = int(request.GET.get('limit',10))
        # 获取数据
        user_list = Users().find_many_by_name(name)
        # 截取数据
        user_list = user_list[:limit]
        res_list = []
        for user in user_list:
            # 将对象中不是字符串的变量值转换为字符串
            user['_id'] = user['_id'].__str__()
            res_list.append(user)
        # 转换为JSON
        res = json.dumps(res_list, indent=4)
        return HttpResponse(res, content_type='application/json')
    except Exception,e:
        res = {
            'info' : '模糊匹配失败指定用户名失败！',
            'reason' : str(e)
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
            'info' : '用户详情获取失败！',
            'reason' : str(e)
        }
        res = json.dumps(res, indent=4)
        return HttpResponse(res, content_type='application/json')



