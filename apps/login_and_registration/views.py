from django.shortcuts import render, redirect
from django.contrib import messages
from django.template import RequestContext
from .models import Users
import bcrypt


def index(request):
    if 'login' in request.session:
        return redirect('/sos')
    if 'index' not in request.session:
        request.session['index'] = 'register'
    return render(request, 'login_and_registration/index.html')

def login(request):
    errors = Users.objects.login_validation(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else:
        logged_in = Users.objects.filter(email=request.POST['email'])
        request.session['login'] = logged_in[0].id
        request.session['name'] = "{} {}".format(logged_in[0].first_name, logged_in[0].last_name)
        if logged_in[0].user_groups_joined.all().count() > 0:
            current_group = logged_in[0].user_groups_joined.all()
            print current_group[0]
            request.session["group"] = current_group[0].id
            return redirect('/sos')
        else:
            return redirect('/sos/join')
    return redirect('/')

def register(request):
    errors = Users.objects.registration_validation(request.POST)
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    hashed_pw = bcrypt.hashpw(request.POST.get("password").encode(), bcrypt.gensalt())
    Users.objects.create(first_name=request.POST.get('first_name', None), last_name=request.POST.get('last_name', None), email=request.POST.get('email', None), password=hashed_pw)
    logged_in = Users.objects.filter(email=request.POST['email'])
    request.session['login'] = logged_in[0].id
    request.session['name'] = "{} {}".format(logged_in[0].first_name, logged_in[0].last_name)
    return redirect('/')

def logout(request):
    request.session['login'] = "bad"
    request.session['group'] = "bad"
    del request.session['login']
    del request.session['group']
    return redirect('/')

def success(request):
    if 'login' not in request.session:
        return redirect('/')
    return render(request, 'login_and_registration/success.html')


def login_form(request):
    request.session['index'] = 'login'
    return redirect('/')

def register_form(request):
    request.session['index'] = 'register'
    return redirect('/')