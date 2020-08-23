from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
def test_show(request):

    all_book = Book.objects.all()

    return render(request, 'bookstore/test_show.html',locals())

def all_book(request):
    #全量获取
    all_book = Book.objects.all()

    #排序
    #all_book = Book.objects.order_by('-price')

    #filter
    #all_book = Book.objects.filter(price=1110.00, title='abc')
    #当返回值 - QuerySet 没有数据时 可按如下方式判断
    #print(all_book.query)

    if not all_book:
        print('---no--book---')

    if len(all_book) == 0:
        print('---no---book 2---')
    #QuerySet 可直接通过query属性 获取当前执行的SQL原生语句
    #print(all_book.query)

    #检查当前查询返回结果 具体类型
    #print(type(all_book))

    #all_book = Book.objects.filter(price=20.00)

    #GET查询
    # book_1 = None
    # try:
    #     book_1 = Book.objects.get(id=1)
    # except:
    #     book_1 = None
    #
    # print(book_1)

    #GET 替代性方案
    book_2 = Book.objects.filter(id=1)
    print(book_2[0])











    return render(request, 'bookstore/all_book.html', locals())


def add_book(request):

    if request.method == 'GET':
        return render(request, 'bookstore/add_book.html')
    elif request.method == 'POST':
        #添加书籍
        title = request.POST.get('title')
        if not title:
            return HttpResponse('Please give me title')
        pub = request.POST.get('pub')
        #指定出版社白名单 - pub_whitelist
        price = request.POST.get('price')
        if not price:
            return HttpResponse('Please give me price')
        market_price = request.POST.get('market_price')
        if not market_price:
            return HttpResponse('Please give me market_price')
        market_price = float(market_price)
        price = float(price)

        market_price = float(request.POST.get('market_price', '999'))

        #title是不是已经存在了
        old_book = Book.objects.filter(title=title)

        if old_book:
            return HttpResponse('Oh~no~This book is already existed !')

        try:
            Book.objects.create(title=title,pub=pub,price=price, market_price=market_price)
        except Exception as e:
            print('---add error---is %s'%(e))

        return HttpResponseRedirect('/bookstore/all_book')

    return HttpResponse('Please use GET or POST !')



def update_book(request, book_id):

    book_id = int(book_id)
    try:
        book = Book.objects.get(id=book_id)
    except Exception as e:
        return HttpResponse('---no book---')

    if request.method == 'GET':


        #filter版本
        # books = Book.objects.filter(id=book_id)
        # if books:
        #     book = books[0]
        # else:
        #     pass
        return render(request, 'bookstore/update_book.html', locals())

    elif request.method == 'POST':
        #更新操作
        price = request.POST.get('price')
        market_price = request.POST.get('market_price')
        if not price or not market_price:
            return HttpResponse('---Please give me price or market_price---')

        price = float(price)
        market_price = float(market_price)
        #修改对象属性
        book.price = price
        book.market_price = market_price
        #存储变化
        book.save()
        return HttpResponseRedirect('/bookstore/all_book')

    return HttpResponse('test update')

def set_cookie_view(request):

    resp = HttpResponse()
    resp.set_cookie('username', 'guoxiaonao', 3600)
    return resp

def get_cookie_view(request):

    value = request.COOKIES.get('username')
    print('my cookie value is', value)
    return HttpResponse('---get---cookie---')


def login(request):

    if request.method == 'GET':
        #获取登录页面
        #检查cookie
        if 'username' in request.COOKIES.keys():
            return HttpResponse('---您已登录---')
        return render(request, 'bookstore/login.html')

    elif request.method == 'POST':
        #处理登录请求
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = User.objects.filter(username=username,password=password)

        if not users:
            #用户名或密码错误
            return HttpResponse('用户名或密码错误')
        user = users[0]
        #session添加 登录状态
        request.session['username'] = username
        resp = HttpResponse('---登录成功---')

        #下次免登陆
        if 'isSaved' in request.POST.keys():
            #选中了 下次免登陆,存cookie
            resp.set_cookie('username', username, 60*60*24*7)

        return resp




def session_view(request):
    #session 赋值
    #request.session['username'] = 'guoxiaonao'

    #session获取数据
    # v = request.session['username']
    # html = 'my session key is username , value is %s'%(v)

    #session删除 指定key
    #del request.session['username']
    #request.session['username']

    #session更改过期时间
    request.session['age'] = 18

    return HttpResponse('---session test is ok ---')
    #return HttpResponse(html)

































































