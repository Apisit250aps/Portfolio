from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def member_system(request):
    
    data = {
        'title':'Member'
    }
    return render(request, 'system/member/member.html', data)
