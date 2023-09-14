from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Business
from django.contrib.auth.decorators import login_required
from users.views import Uzer


@login_required(login_url='/user/login', redirect_field_name='next')
def register_business(request):
    if request.method == "POST":
        business_name = request.POST.get("business_name")
        business_type = request.POST.get("business_type")
        description = request.POST.get("description")
        location = request.POST.get("location")
        email_contact = request.POST.get("email_contact")
        phone_contact = request.POST.get("phone_contact")
        status = 1
        if Uzer.objects.filter(id=request.user.id).exists():
            user = Uzer.objects.get(id=request.user.id)
            new_business = Business.objects.create(
                business_name=business_name,
                business_type=business_type,
                description=description,
                location=location,
                email_contact=email_contact,
                phone_contact=phone_contact,
                status=status,
                user=user)
            new_business.save()
        next_url = request.GET.get('next', '/user/home')
        print(next_url)
        return redirect(next_url)
    return render(request, "create_business.html")


def business_profile(request):
    """Display info about the business"""
    pass
