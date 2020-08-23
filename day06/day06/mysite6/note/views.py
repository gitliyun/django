from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note
from user.models import User

# Create your views here.
def note_index(request):

    return render(request, 'note/index.html', locals())

def list_view(request):

    return HttpResponse('list test')


def check_logging(fn):
    def wrap(request, *args, **kwargs):
        #检查用户是否登录
        #1, 先检查session
        if 'username' not in request.session:
            if 'username' not in request.COOKIES:
                return HttpResponseRedirect('/user/login')
            else:
                #赋值回session
                request.session['username'] = request.COOKIES['username']

        return fn(request, *args, **kwargs)
    return wrap


@check_logging
def add_view(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')

    elif request.method == 'POST':
        #处理提交数据
        title = request.POST.get('title')
        content = request.POST.get('content')
        #存数据
        username = request.session.get('username')
        user = User.objects.get(username=username)
        note = Note(user=user)
        note.title = title
        note.content = content
        note.save()
        return HttpResponseRedirect('/note/')













