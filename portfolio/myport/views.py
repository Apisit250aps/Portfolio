from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def portfolio(request):
    
    
    data = {
        'title':'portfolio'
    }
    return render(request, 'portfolio.html', data)
    