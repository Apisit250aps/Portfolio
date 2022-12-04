from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.contrib.auth.models import User
from django.http import request
# Create your views here.

def portfolio(request):
    
    data = {
        'title':'portfolio'
    }
    return render(request, 'portfolio.html', data)

def workpage(request):
    data = {
        'title':'Work'
    }
    
    return render(request, 'form/workpost.html', data)

def form_get(request):
    
    f_name = request.POST.get('fname', None)
    l_name = request.POST.get('lname')
    _username = request.POST.get('username')
    _email = request.POST.get('email')
    _password = request.POST.get('password')
    _cf_password = request.POST.get('cf_password')
    
    state = '0000'
    if f_name == None:
        print(state)
    else :
        if len(_password) < 6:
            state = '0011'
        else :
            if _cf_password != _password:
                state = '0001'
            else :
                if User.objects.filter(username=_username).exists():
                    state = '0101'
                elif User.objects.filter(email=_email).exists():
                    state = '0111'
                else : 
                    user = User.objects.create_user(
                        first_name = f_name,
                        last_name = l_name,
                        username=_username,
                        email=_email,
                        password=_password
                    )
                    user.save()
                    state = '0002'
                    return redirect('workpost')
    data = {
        'title':'Register',
        'state':state
    }
    print(state)
    return render(request, 'form/form_get.html', data)

def table(request):
    members = Member.objects.all()
    
    
    
    data = {
        'title':'Table',
        'member':members
    }
    return render(request, 'form/table.html', data)