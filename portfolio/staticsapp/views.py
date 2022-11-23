from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def homepage(request):
    data = {
        "title":"Portfolio"
    }
    return render(request, 'portfolio.html', data)

def library(request):
    data = {
        "title":"Library"
    }
    return render(request, 'statics/works1/library.html', data)