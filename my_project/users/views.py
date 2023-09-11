from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import randint
from django.contrib.auth.models import User as Uzer
from .models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def user_signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        if Uzer.objects.filter(email=email).exists():
            return HttpResponse("User email already exists. Try another email")
        else:
            while True:
                user_name = f"{first_name}{randint(1, 999)}"
                if not Uzer.objects.filter(username=user_name).exists():
                    break
            new_user = Uzer.objects.create_user(
                user_name,
                email,
                password,
                first_name=first_name,
                last_name=last_name
            )
            new_user.save()
            return redirect("/user/login")
    return render(request, "signup.html")


def user_login(request):
    if request.method == "POST":
        user_name = request.POST['user_name']
        password = request.POST['password']
        user = authenticate(username=user_name, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            return redirect("/user/login")
    return render(request, "users/login.html")


def user_logout(request):
    logout(request)
    return redirect('/')
