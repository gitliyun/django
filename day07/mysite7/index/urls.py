from django.conf.urls import url
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    #http://127.0.0.1:8000/index/test_cache/100
    #url(r'^test_cache$', cache_page(15)(views.test_cache)),
    url(r'^test_cache$',views.test_cache)
]