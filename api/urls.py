from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hello/', views.hello),
    url(r'^articlelist', views.articleList),
    url(r'^article', views.articleDetail),
    url(r'^usercheck', views.userCheck),
    url(r'^userlist$', views.userList),
    url(r'^user$', views.userDetail),
    url(r'^reguser', views.regUser),
    url(r'^userlistbyid$',views.userListByID),

]

