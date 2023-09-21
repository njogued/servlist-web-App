from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Business
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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
        return redirect('/user/home')
    return render(request, "create_business.html")


def business_profile(request, business_id):
    """Display info about the business"""
    if request.method == "POST":
        business_name = request.POST.get("business_name")
        business_type = request.POST.get("business_type")
        description = request.POST.get("description")
        location = request.POST.get("location")
        email_contact = request.POST.get("email_contact")
        phone_contact = request.POST.get("phone_contact")
        business = Business.objects.get(business_id=business_id)
        if business_name:
            business.business_name = business_name
        if business_type:
            business.business_type = business_type
        if description:
            business.description = description
        if location:
            business.location = location
        if email_contact:
            business.email_contact = email_contact
        if phone_contact:
            business.phone_contact = phone_contact
        business.save()
        return JsonResponse({"message": "Successfully edited"})
    if request.method == "DELETE":
        business = Business.objects.get(business_id=business_id)
        business.delete()
        return redirect("/user/home")

    try:
        business = Business.objects.get(business_id=business_id)
        context = {'business': business}
        owner = Uzer.objects.get(id=business.user_id)
        context['owner'] = owner
        print(request.user.username)
        print(context['business'].__dict__)
        print(context['owner'].__dict__)
        return render(request, 'business_profile.html', context)
    except Business.DoesNotExist:
        return HttpResponse("Business Does Not Exist")

def all_businesses(request):
    businesses = Business.objects.order_by('date_created')
    paginator = Paginator(businesses, 5)  
    page_number = request.GET.get('page')
    page_businesses = paginator.get_page(page_number)

    businesses = {
        'page_businesses': page_businesses,  # This variable is passed to the template
    }

    return render(request, 'all_businesses.html', businesses)

def search_results(request):
    """Display search results"""
    if request.method == "POST":
        search_keyword = request.POST.get("search_keyword")
        businesses = Business.objects.filter(business_type__icontains=search_keyword)
        paginator = Paginator(businesses, 5)  
        page_number = request.GET.get('page')
        page_businesses = paginator.get_page(page_number)

        businesses = {
            'page_businesses': page_businesses,  # This variable is passed to the template
        }
        return render(request, 'all_businesses.html', businesses)
    return redirect("/user/home")