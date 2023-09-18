from django.urls import path
from .views import user_signup, user_profile, user_login, user_logout, index
from businesses.views import register_business

urlpatterns = [
    path("signup", user_signup, name="SignUp"),
    path("login", user_login, name="Login"),
    path("logout", user_logout, name="Logout"),
    path("home", index, name="User Home"),
    path("register", register_business, name="Register"),
    path("<str:user_name>", user_profile, name="User Profile"),
]
