from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def get_speed(request):
    if request.method == 'GET':
        return HttpResponse('Hello World!')
