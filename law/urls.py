from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/auth/$', views.auth_view, name='auth'),
    url(r'^review/$', views.review_contract, name='review'),
]