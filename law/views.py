#import statements
#python first
import hashlib, datetime, random
#django second
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User

#your apps

#local
from models import UserProfile, ReviewRequest
from forms import RegistrationForm, ReviewRequestForm


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
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            user = User.objects.get(username=username)
            
            new_profile = UserProfile(user = user, activation_key = activation_key, key_expires = key_expires)
            new_profile.save()
            # email starts here
            subject = 'Confirm Registration'
            message = "Hi, %s Thanks for signing up. Activate you account by clicking this link within 48 hours. http://127.0.0.1:8000/law/%s Confirm your email address with the following" % (username, activation_key)
            msg = "Hey %s, thanks for signing up. To activate your account, click this link within \
            48hours http://127.0.0.1:8000/law/accounts/confirm/%s" % (username, activation_key)

            from_email = settings.EMAIL_HOST_USER
            to_email = [settings.EMAIL_HOST_USER]
            send_mail(subject, msg, from_email, to_email, fail_silently=True)

            return HttpResponseRedirect(reverse('law:register_success'))
        else:
            # return render(request, 'law/registration/auth.html')
            args['form'] = RegistrationForm()

    return render_to_response('law/registration/register.html', args) 

def register_success(request):
    return render_to_response('law/index.html')

def register_confirm(request, activation_key):
    if request.user.is_authenticated(): #if user is already logged in 
        HttpResponseRedirect(reverse('law:index'))
    
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key) # check if the user profile exist
    
    if user_profile.key_expires < timezone.now():
        return render_to_response('law/registration/confirm_expired.html')
    
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('law/registration/confirmation_email.html')


