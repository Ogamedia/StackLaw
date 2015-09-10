from django.shortcuts import render, render_to_response
from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.core.context_processors import csrf


# Create your views here.
def index(request):
    user = request.user.username
    return render_to_response('law/index.html', {'username': user})

def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('law/registration/login.html', c)

def auth_view(request):
    username = request.POST.get('username', ' ')
    password = request.POST.get('password', ' ')
    user = auth.authenticate(username = username, password = password)
    
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('law:index'))
    else:
        return render(request, 'law/registration/auth.html')