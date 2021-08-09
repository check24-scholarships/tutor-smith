from django.shortcuts import render, redirect
from django.http import HttpResponse

import datetime

def hello_world_temp(request):
    return render(
        request, 'hello.html', context={'time': datetime.datetime.now()}
    )

# Handels incoming GET & POST requests on the register view. 
def register(request):
    __context = {'error_msg': None}
    if request.method == "GET":
        __context['error_msg'] = None
        return render(request, 'register.html', context=__context)
    if request.method == "POST":
        __context['error_msg'] = "Not Implemented"
        return render(request, 'register.html', context=__context)