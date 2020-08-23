import csv

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .models import UserInfo

# Create your views here.
def user_add(request):
    #添加用户
    if request.method == 'GET':
        #拿页面
        return render(request, 'index/user_add.html')
    elif request.method == 'POST':
        #添加用户
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        UserInfo.objects.create_user(username=username, password=password, email=email)

        return HttpResponseRedirect('/index/add')

def user_show(request):
    #显示所有用户
    all_user = UserInfo.objects.all()
    return render(request, 'index/user_show.html', locals())

def user_csv(request):
    #生成csv文本
    #改变response的content-type头
    res = HttpResponse(content_type='text/csv')
    #添加 Content-Disposition 头
    res['Content-Disposition'] = 'attachment;filename="allUser.csv"'

    #获取数据库中的数据
    all_user = UserInfo.objects.all()
    #生成csv writer对象
    writer = csv.writer(res)
    #csv 表头
    writer.writerow(['username', 'email'])
    #写具体数据
    for user in all_user:
        writer.writerow([user.username, user.email])
    return res





















