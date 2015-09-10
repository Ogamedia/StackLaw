from django.shortcuts import render, get_object_or_404, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf


# Create your views here.
def index(request):
    return render(request, 'law/index.html')

def login(request):
    c = {}
    c.update(csrf(request))
    render_to_response('login.html', c)

def auth_view(request):
    username = request.POST.get('username', ' ')
    password = request.POST.get('password', ' ')
    user = auth.authenticate(username = username, password = password)
    
    if user is not None:
        auth.login(requests, user)
        return HttpResponseRedirect('law/index')
    else:
        return HttpResponseRedirect('law/registration/auth.html')