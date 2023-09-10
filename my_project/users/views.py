from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import randint
from .models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def user_signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        user_name = f"{first_name}{randint(1, 999)}"
        if User.objects.filter(email=email).exists():
            return HttpResponse("User email already exists. Try another email")
        else:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                user_name=user_name
            )
            new_user.save()
            return HttpResponse("User Created")
    return render(request, "signup.html")


def user_login(request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(user_name=user_name, password=password)
        if user:
            login(request, user)
            return HttpResponse("Logged in")
        else:
            return redirect('/login')


def user_logout(request):
    logout(request)
    return redirect('/')
