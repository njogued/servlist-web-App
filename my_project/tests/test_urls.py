from django.test import SimpleTestCase
from django.urls import resolve, reverse
from businesses.views import register_business, business_profile, all_businesses
from users.views import user_profile, user_login, user_signup, index


class TestUrls(SimpleTestCase):
    """Test urls used for this project"""

    def test_new_business(self):
        url = reverse('Register Business')
        self.assertEquals(resolve(url).func, register_business)

    def test_business_profile(self):
        url = reverse('Business Profile', args=[99])
        self.assertEquals(resolve(url).func, business_profile)

    def test_all_businesses(self):
        url = reverse('All Businesses')
        self.assertEquals(resolve(url).func, all_businesses)

    def test_user_profile(self):
        url = reverse("User Profile", args=["servlist"])
        self.assertEquals(resolve(url).func, user_profile)

    def test_user_signup(self):
        url = reverse("SignUp")
        self.assertEquals(resolve(url).func, user_signup)

    def test_user_login(self):
        url = reverse("Login")
        self.assertEquals(resolve(url).func, user_login)

    def test_user_home(self):
        url = reverse("User Home")
        self.assertEquals(resolve(url).func, index)
