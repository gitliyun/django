from django.http import HttpResponseRedirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMW(MiddlewareMixin):

    def process_request(self, request):
        #校验用户登录信息
        #白名单
        w_list = ['/user/reg', '/user/login', '/user/logout', '/user/test']

        if request.path in w_list:
            return None

        if 'username' not in request.session:
            if 'username' not in request.COOKIES:
                print('---login mw check return---')
                return HttpResponseRedirect('/user/login')
            else:
                #赋值回session
                request.session['username'] = request.COOKIES['username']



class VisitLimitMW(MiddlewareMixin):

    #redis? key - 生命周期  1分钟
    count_dict = {}
    def process_request(self,request):
        #检查请求次数并进行拦截
        #取出访问者ip地址
        ip_add = request.META['REMOTE_ADDR']
        # /user/test
        if request.path != '/user/test':
            return None
        count = self.count_dict.get(ip_add, 0)
        count += 1
        self.count_dict[ip_add] = count
        if count > 5:
            return HttpResponse('You guofen le!!! %s'%(count))





















