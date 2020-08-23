from django.conf.urls import url
from . import views

urlpatterns = [
    #http://127.0.0.1:8000/index/add
    url(r'^add$', views.user_add),
    #http://127.0.0.1:8000/index/show
    url(r'^show$', views.user_show),
    #http://127.0.0.1:8000/index/csv
    url(r'^csv$', views.user_csv)
]