from django.shortcuts import render, redirect
from django.http import HttpResponse

import datetime

# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, World!")

def hello_world_temp(request):
    return render(request, 'hello.html', context={'time':datetime.datetime.now()})