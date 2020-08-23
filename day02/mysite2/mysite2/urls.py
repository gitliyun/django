"""mysite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test_get$', views.test_get),
    url(r'^sum$', views.sum_view),
    url(r'^test_post_form$', views.test_post),
    url(r'^test_login_html$', views.test_login_html),
    url(r'^test_html$', views.test_html),
    url(r'^test_if$', views.test_if),
    #http://127.0.0.1:8000/mycal
    url(r'^mycal$', views.mycal_view),
    url(r'^test_base$', views.test_base),
    url(r'^test_music$', views.test_music),
    url(r'^test_sport$', views.test_sport)

]
