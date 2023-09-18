from django.shortcuts import render


def index(request):
    return render(request, 'landingpage.html')


def contacts(request):
    nextval = request.GET.get('next')
    print(nextval)
    return render(request, "contactus.html")


def about(request):
    return render(request, 'aboutus.html')
