from django.http import HttpResponse
from django.shortcuts import render

get_form='''
<form method='get' action="/test_get_form">
    姓名:<input type="text" name="uname">
    <input type="submit" value="干">
</form>
'''

post_form='''
<form method='post' action="/test_post_form">
    姓名:<input type="text" name="uname">
    密码:<input type="text" name="password">
    <input type="submit" value="干post">
</form>
'''


def test_get(request):
    #测试 获取查询字符串
    #http://127.0.0.1:8000/test_get?a=100&b=200
    if request.method == 'GET':
        #获取方式1  request.GET[参数名]
        #a = request.GET['a']

        #获取方式2  request.GET.get('参数名',‘默认值’); 如果不给默认值 返回None
        # a = request.GET.get('a')
        # html = 'a= %s'%(a)

        #获取方式3  requets.GET.getlist('参数名'), 在key为多个value使用该方式
        # a = request.GET.getlist('a')
        # html = 'a= %s' % (a)

        #输出 request.GET
        # g = str(dict(request.GET))
        # html = 'request.GET = %s'%(g)

        #测试 form get版本
        html = get_form
        return HttpResponse(html)

    elif request.method == 'POST':
        pass
    else:
        pass
    return HttpResponse('---test---error---')


def sum_view(request):

    if request.method == 'GET':
        try:
            start = request.GET.get('start', '0')
            start = int(start)
            step = request.GET.get('step', '1')
            step = int(step)
            stop = request.GET.get('stop')
            if not stop:
                return HttpResponse('Please give me stop value !')
            stop = int(stop)
            mysum = sum(range(start,stop,step))
            html = '结果是： %d'%(mysum)
            return HttpResponse(html)
        except Exception as e:
            print('sum error is %s'%(e))
            return HttpResponse('Please use normal input!')

    return HttpResponse('---Please use Http get !!!')


def test_post(request):

    if request.method == 'GET':
        #浏览器来获取数据
        return HttpResponse(post_form)

    elif request.method == 'POST':
        uname = request.POST.get('uname')
        return HttpResponse('--- %s post is ok---'%(uname))

    return HttpResponse('---Please use GET or POST !')

def test_login_html(request):

    #1 导入loader
    # from django.template import loader
    # #2 通过loader加载模板
    # t = loader.get_template('login.html')
    # #3 执行render 转化成字符串
    # html = t.render({'name':'guoxiaonao'})
    # #4 将内容响应给浏览器
    # return HttpResponse(html)

    #方案2
    from django.shortcuts import render
    return render(request, 'login.html', {'name': 'guoxiaonao_render'})


def test_html(request):

    dic = {}
    dic['int'] = 3
    dic['str'] = 'guoxiaonao'
    dic['lst'] = ['北京','上海','天津']
    #dic['lst'] = []
    dic['d'] = {'name':'guoxiaonao', 'age':18}
    dic['say_hi'] = say_hi
    dic['class_obj'] = Dog()
    dic['script'] = '<script>alert(11)</script>'
    return render(request, 'test_html.html', dic)

class Dog:
    def say(self):
        return 'wang wang!'



def say_hi():

    return 'Hi everyone'


def test_if(request):

    dic = {'x': 10}
    return render(request, 'test_if.html', dic)

def mycal_view(request):
    #get 访问 获取页面
    if request.method == 'GET':
        return render(request, 'mycal.html')
    elif request.method == 'POST':
        #计算数据
        x = int(request.POST.get('x', 0))
        y = int(request.POST.get('y', 0))
        op = request.POST.get('op')
        result = 0
        if op == 'add':
            result = x + y
        elif op == 'sub':
            result = x - y
        elif op == 'mul':
            result = x * y
        elif op == 'div':
            result = x / y
        # dic = {}
        # dic['op'] = op
        # dic['x'] = x
        # dic['y'] = y
        # dic['result'] = result
        return render(request, 'mycal.html',locals())


def test_base(request):
    lst= ['zhong','qiu','kuai','le']
    return render(request, 'base.html',locals())

def test_music(request):

    return render(request, 'music.html')

def test_sport(request):

    return render(request, 'sport.html')














    return HttpResponse('--Please use GET or POST--')






























