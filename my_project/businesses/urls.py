from django.urls import path
from .views import register_business, business_profile

urlpatterns = [
    path("register", register_business, name="Register Business"),
    path("profile", business_profile, name="Business Profile"),
]
