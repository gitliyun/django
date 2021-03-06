from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/bookstore/test_show
    url(r'^test_show$', views.test_show),
    #http://127.0.0.1:8000/bookstore/all_book
    url(r'^all_book$', views.all_book),
    #http://127.0.0.1:8000/bookstore/add_book
    url(r'^add_book$', views.add_book),
    url(r'^update_book/(\d+)$', views.update_book)
]