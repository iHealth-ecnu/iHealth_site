#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse
from models import *
import json

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
    # 提取参数
    id = request.GET.get('id',None)
    if id == None:
        return HttpResponse('请提供 id 参数!')
    # 获取数据
    article = Articles().find_one(id=id)
    # 转换为 JSON
    del article['_id']
    del article['intro']
    article['pubdate'] = article['pubdate'].__str__()
    article['content'] = article['content'].strip()
    res = json.dumps(article, indent=4)
    return HttpResponse(res, content_type='application/json')
