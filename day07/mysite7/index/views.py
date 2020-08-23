from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import time

# Create your views here.
#@cache_page(60)
def test_cache(request):

    #测试缓存
    # t1 = time.time()
    # #time.sleep(5)
    # html = 't1 is %s'%(t1)
    # return HttpResponse(html)
    print('----this is test cache views ----')
    #测试缓存页面局部
    return render(request, 'index/test_cache.html', locals())






