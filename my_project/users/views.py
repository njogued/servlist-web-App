from django.http import HttpResponse
from django.shortcuts import render, redirect
from random import randint
from django.contrib.auth.models import User as Uzer
from .models import User
from businesses.models import Business
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/user/login')
def index(request):
    return render(request, 'index.html')


def user_signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['user_name']
        email = request.POST['email']
        password = request.POST['password']
        if Uzer.objects.filter(email=email).exists():
            return HttpResponse("User email already exists. Try another email")
        else:
            if Uzer.objects.filter(username=user_name).exists():
                return HttpResponse("Username taken")
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
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect("/user/home")
        else:
            return redirect("/user/login")
    return render(request, "users/login.html")


def user_logout(request):
    logout(request)
    return redirect('/')


def my_profile(request):
    return render(request, 'user_profile.html')


def user_profile(request, user_name):
    if user_name == request.user.username:
        my_profile(user_name)
    else:
        user_id = request.user.id
        bs_data = Business.objects.filter(user_id=user_id)
        userbusinesses = list(bs_data)
        context = {'owned': userbusinesses}
        return render(request, 'user_profile.html', context)
