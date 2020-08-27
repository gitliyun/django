#file:bookstore/urls.py

from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^book$',views.add_view),
    url(r'^name$',views.name_view),
    url(r'^aook',views.aa_view),
]