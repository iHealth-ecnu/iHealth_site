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
    url(r'^updateUpvote$',views.doUpvote),
    url(r'^changeNickname$',views.changeNickname),
    url(r'^changePhone$',views.changePhone),
    url(r'^changeName$',views.changeName),
    url(r'^changeSex$',views.changeSex),
    url(r'^changePassword$',views.changePassword),
    url(r'^changeBirthday$',views.changeBirthday),
    url(r'^addMedicalRecord$',views.addMedicalRecord),
    url(r'^test$',views.test),
]

