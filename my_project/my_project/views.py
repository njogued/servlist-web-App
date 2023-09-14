from django.http import HttpResponse
from django.shortcuts import render, redirect

# @app.route('/')


def index(request):
    return render(request, 'index.html')
