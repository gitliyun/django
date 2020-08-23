from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/user/reg
    url(r'^reg$', views.reg_view),
    #http://127.0.0.1:8000/user/login
    url(r'^login$', views.login_view),
    #http://127.0.0.1:8000/user/logout
    url(r'^logout$', views.logout_view),
    #http://127.0.0.1:8000/user/test 测试访问次数【中间件】
    url(r'^test', views.user_test)
]