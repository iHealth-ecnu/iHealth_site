from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hello/', views.hello),
    url(r'^articlelist', views.articleList),
    url(r'^article', views.articleDetail),
    url(r'^usercheck', views.userCheck),
    url(r'^userlist', views.userList),
]

