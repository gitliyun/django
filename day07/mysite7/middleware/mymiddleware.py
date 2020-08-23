from django.utils.deprecation import MiddlewareMixin

class MyMW(MiddlewareMixin):

    def process_request(self, request):
        #请求到达urls主路由之前 执行当前方法
        #None 正常返回
        #HttpResponse 则跳出django 直接返回
        print('MyMW process_request do---')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        #None 正常返回
        #HttpResponse 则跳出django 直接返回
        print('MyMW process_views do ---')

    def process_response(self, request, response):
        #必须返回 response
        print('MyMW process_response do ---')
        return response



class MyMW2(MiddlewareMixin):

    def process_request(self, request):
        #请求到达urls主路由之前 执行当前方法
        #None 正常返回
        #HttpResponse 则跳出django 直接返回
        print('MyMW2 process_request do---')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        #None 正常返回
        #HttpResponse 则跳出django 直接返回
        print('MyMW2 process_views do ---')

    def process_response(self, request, response):
        #必须返回 response
        print('MyMW2 process_response do ---')
        return response