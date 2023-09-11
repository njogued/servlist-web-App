from django.shortcuts import render
from django.http import HttpResponse
from .forms import CreateBusinessForm
from .models import Business
# from django.contrib.auth import models
# # Create your views here.
# user = models.User()


def register_business(request):
    """Function to handle new business registration"""
    if request.method == 'POST':
        form = CreateBusinessForm(request.POST)
        if form.is_valid():
            business_info = {}
            fields = ["business_name",
                      "business_type",
                      "description",
                      "location",
                      "email_contact",
                      "phone_contact"]
            for field in fields:
                business_info[field] = request.POST.get(field)
            new_business = Business(**business_info)
            new_business.status = 1
            new_business.save()
        return HttpResponse("New Business Created")
    context = {}
    context['form'] = CreateBusinessForm()
    return render(request, "create.html", context)


def business_profile(request):
    """Display info about the business"""
    pass
