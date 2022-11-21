from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def homepage(request):
    data = {
        "title":"Homepage"
    }
    return render(request, 'port_1/main.html', data)

def library(request):
    data = {
        "title":"Library"
    }
    return render(request, 'port_2/library.html')