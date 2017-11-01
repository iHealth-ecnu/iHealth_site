#coding=utf8
from django.db import models
from django.conf import settings
from bson.objectid import ObjectId
import pymongo

class Articles():
    def __init__(self):
        '''初始化'''
        # 连接 mongo 数据库，获得数据指定集合
        self.client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s'%(settings.
MONGO_USER,settings.MONGO_PWD,settings.MONGO_HOST,settings.MONGO_PORT,settings.
MONGO_AUTHDB))[settings.MONGO_DBNAME]
        self.articles = self.client['articles']
    
    def find_one(self,id):
        '''获取指定数据'''
        article = self.articles.find_one({"_id": ObjectId(id)})
        return article

    def find_all(self):
        '''返回全部文章'''
        '''默认按照倒序排列，即取出最新插入的文章'''
        article_list = self.articles.find().sort('_id', pymongo.DESCENDING)
        return article_list

    def updateRead(self,id=None,cnt=1):
        '''阅读量+1'''
        if id == None:
            raise Exception,'请提供 id 参数!'
        self.articles.update_one({'_id':ObjectId(id)},{'$inc':{'read':cnt}})    

class Users():
    def __init__(self):
        '''初始化'''
        # 连接 mongo 数据库，获得数据指定集合
        self.client = pymongo.MongoClient('mongodb://%s:%s@%s:%d/%s'%(settings.
MONGO_USER,settings.MONGO_PWD,settings.MONGO_HOST,settings.MONGO_PORT,settings.
MONGO_AUTHDB))[settings.MONGO_DBNAME]
        self.users = self.client['users']
    
    def find_one(self,id):
        '''获取指定数据'''
        user = self.users.find_one({"_id": ObjectId(id)})
        return user

    def find_one_by_email(self,email):
        '''获取指定数据'''
        user = self.users.find_one({"email": email})
        return user

    def find_all(self):
        '''返回全部用户数据'''
        user_list = self.users.find()
        return user_list


