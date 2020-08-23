from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/note/  显示用户所有笔记页
    url(r'^$', views.list_view),

    #http://127.0.0.1:8000/note/index  主页
    url(r'^index$', views.note_index),

    #http://127.0.0.1:8000/note/add
    url(r'^add$', views.add_view)


]