from django.urls import path
from .views import register_business, business_profile
from . import views

urlpatterns = [
    path("register", register_business, name="Register Business"),
    path("<int:business_id>", business_profile, name="Business Profile"),
    path('businesses/', views.all_businesses, name='All Businesses'),
]
