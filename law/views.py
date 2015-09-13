#import statements
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views import generic
from forms import RegistrationForm, ReviewRequestForm

#python first
#django second
#your apps
#local

# Create your views here.
def index(request):
    user = request.user
    return render_to_response('law/index.html', {'user': user})

def review_requests(request):
    if request.POST:
        form = ReviewRequestForm(request.POST)
        if form.is_valid():
            form.save()
            
            return HttpResponseRedirect(reverse('law:index'))
    
    else:
        form = ReviewRequestForm()
    
    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render_to_response('law/request/create.html' ,args)

# def review_requests(request):
#     pass

# ================== authorisation ======================
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

def logout(request):
    auth.logout(request)
    return render_to_response('law/registration/logout.html')

@login_required(redirect_field_name='', login_url='law:login')
def review_contract(request):
    return render(request, 'law/review_contract.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            subject = 'Confirm Registration'
            message = "Hi,/n Confirm your email address with the following"
            from_email = settings.EMAIL_HOST_USER
            to_email = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_email, fail_silently=True)

            return HttpResponseRedirect(reverse('law:register_success'))
        else:
            return render(request, 'law/registration/auth.html')
    
    args = {}
    args.update(csrf(request))
    args['form'] = RegistrationForm()

    return render_to_response('law/registration/register.html', args) 

def register_success(request):
    return render_to_response('law/index.html')


