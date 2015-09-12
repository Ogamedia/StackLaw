from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^review/$', views.review_contract, name='review'),
    url(r'^requests/$', views.review_requests, name='requests'),
    # url(r'^create/$', views.create_contract, name='create'),
    
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/auth/$', views.auth_view, name='auth'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register_success/$', views.register_success, name='register_success'),
    
]