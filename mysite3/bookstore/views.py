from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

#file:bookstore/views.py

from . import models

def add_view(request):
    try:
        #方法 1
        abook = models.Book.objects.create(
            title='西游记',price=20,market_price=25,
            pub='清华大学出版社')
        return HttpResponse("添加图书成功!")
        # abook = models.Book(price=98)
        # abook.title='西游记'
        # abook.market_price=25
        # abook.pub='清华大学出版社'
        # abook.save()#真正执行sql语句
    except Exception as err:
        return HttpResponse("添加图书失败！")

def name_view(request):
    try:
        #方法 1
        aname = models.Author.objects.create(
            name='王老师', age=28, email='wangweichao@tedu.cn')
        # abook = models.Book(price=98)
        # abook.title='西游记'
        #aname.save()#真正执行sql语句
        return HttpResponse("添加作者成功!")
    except Exception as err:
        return HttpResponse("添加作者失败！")

def aa_view(request):
    try:
        #方法 1
        abook = models.Aook.objects.create(
            title='西游记',price=20,market_price=25,
            pub='清华大学出版社')
        return HttpResponse("添加图书成功!")
        # abook = models.Book(price=98)
        # abook.title='西游记'
        # abook.market_price=25
        # abook.pub='清华大学出版社'
        # abook.save()#真正执行sql语句
    except Exception as err:
        return HttpResponse("添加图书失败！")
