from django.urls import path
from .views import user_signup, user_login, user_logout
from . import views

urlpatterns = [
    path("signup", views.user_signup, name="SignUp"),
    path("login", views.user_login, name="Login"),
    path("logout", views.user_logout, name="Logout"),
    path("", views.user_login, name="User Home")
]