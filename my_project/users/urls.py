from django.urls import path
from .views import user_signup, user_login, user_logout, index

urlpatterns = [
    path("signup", user_signup, name="SignUp"),
    path("login", user_login, name="Login"),
    path("logout", user_logout, name="Logout"),
    path("home", index, name="User Home")
]
