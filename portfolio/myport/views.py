from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth

from django.http import request
from django.contrib import messages
# Create your views here.

from datetime import datetime


def portfolio(request):

    data = {
        'title': 'portfolio'
    }
    return render(request, 'portfolio.html', data)


def workpage(request):
    post_content = request.GET.get('post', None)
    posts = Post.objects.all()

    print(User.first_name)
    print(post_content)
    post_dist = {'post_text':post_content, 'post_date':datetime.now(), 'post_by':User.objects.name}
    if 'post_content' not in request.GET:
        print("Not null")
    else:
        if post_content == '':
            print("Empty")
       
        else:
            
            
            Post.objects.raw('SELECT  post_text, post_date, post_by FROM myport_post')
    #         return redirect('/workpage')

    data = {
        'title': 'Work',
        "post": posts
    }

    return render(request, 'form/workfeed.html', data)

def posting(request):
    pass

def loginForm(request):
    _username = request.POST.get('username')
    _password = request.POST.get('password')

    data = {
        'title': 'Login'
    }

    return render(request, 'form/form_login.html', data)


def login(request):
    _username = request.POST['username']
    _password = request.POST['password']
    if _username == '' or _password == '':
        messages.warning(request, "Empty Entry")
        return redirect('/loginform')
    else:
        user = auth.authenticate(username=_username, password=_password)
        if user is not None:

            auth.login(request, user)
            return redirect('/workpost')
        else:
            messages.info(request, "Not data")
            return redirect('/loginform')


def logout(request):
    auth.logout(request)
    return redirect('/workpost')


def form_get(request):
    f_name = request.POST.get('fname')
    l_name = request.POST.get('lname')
    _username = request.POST.get('username')
    _email = request.POST.get('email')
    _password = request.POST.get('password')
    _cf_password = request.POST.get('cf_password')
    state = '0000'
    if 'fname' not in request.POST:
        print(state)
    else:
        if f_name == '' or l_name == '' or _username == '' or _email == '' or _password == '':
            messages.warning(request, "Entry is empty")
        else:
            if len(_password) < 6:
                state = '0011'
                messages.warning(request, 'Low Security')
            else:
                if _cf_password != _password:
                    state = '0001'
                    messages.warning(request, 'Password is not match')
                else:
                    if User.objects.filter(username=_username).exists():
                        messages.warning(request, "Can't use this Username")
                        state = '0101'
                    elif User.objects.filter(email=_email).exists():
                        state = '0111'
                        messages.warning(request, "Can't use this Email")
                    else:
                        user = User.objects.create_user(
                            first_name=f_name,
                            last_name=l_name,
                            username=_username,
                            email=_email,
                            password=_password
                        )
                        user.save()
                        state = '0002'
                        return redirect('/workpost')
    data = {
        'title': 'Register',
        'state': state
    }
    print(state)
    return render(request, 'form/form_get.html', data)


def table(request):
    members = Member.objects.all()

    data = {
        'title': 'Table',
        'member': members
    }
    return render(request, 'form/table.html', data)
