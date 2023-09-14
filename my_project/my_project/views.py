from django.shortcuts import render


def index(request):
    return render(request, 'landingpage.html')


def contacts(request):
    return render(request, "contactus.html")


def about(request):
    return render(request, 'aboutus.html')
