from django.test import TestCase, Client
from users.views import Uzer
from django.urls import reverse


class TestViews(TestCase):
    """Test the views used in our app"""

    def setUp(self):
        """Set up the client"""
        self.client = Client()
        self.login_url = reverse("Login")
        self.signup_url = reverse("SignUp")
        self.user_profile_url = reverse("User Profile", args=["servlist"])
        self.test_user = self.client.post(
            self.signup_url, {
                "first_name": "Test",
                "last_name": "User",
                "user_name": "TestUser",
                "email": "testuser123@mail.com",
                "password": "TestUser123!"
            }
        )

    def test_user_login_GET(self):
        """Tests if login_url is accessible"""
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_user_login_POST_correct(self):
        """Test whether a user with the right credentials
        is redirected to user home"""
        response = self.client.post(self.login_url, {
            "user_name": "TestUser",
            "password": "TestUser123!",
        })
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/user/home')

    def test_user_login_POST_wrong(self):
        """Test whether user is redirected to login again
        wrong credentials"""
        response = self.client.post(self.login_url, {
            "user_name": "TestUser",
            "password": "WrongPassword123!",
        })
        self.assertEquals(response.url, '/user/login')
        self.assertEquals(response.status_code, 302)

    def test_user_signup_GET(self):
        """Tests if signup_url is accessible"""
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_user_profile_GET(self):
        """Test if nonexistent user redirects"""
        response = self.client.get(self.user_profile_url)
        url = reverse("User Profile", args=["WrongUser"])
        response_two = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response_two.status_code, 302)

    def test_user_profile_exists_GET(self):
        """Tests if userprofile for existing user is shown"""
        user_profile_url_user_name = reverse('User Profile', args=['TestUser'])
        response = self.client.get(user_profile_url_user_name)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "user_profile.html")

    def test_user_profile_edit_POST(self):
        """Test if a logged in user can edit their profile"""
        self.client.login(username="TestUser", password="TestUser123!")
        user_profile_url_user_name = reverse('User Profile', args=['TestUser'])
        response = self.client.post(user_profile_url_user_name, {
            "first_name": "Updated",
            "last_name": "Uzer",
            "email": "newtestuseremail@mail.com"
        })
        response_data = response.json()
        updated_user = Uzer.objects.get(username='TestUser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, {"message": "Successfully updated"})
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Uzer")
        self.assertEqual(updated_user.email, "newtestuseremail@mail.com")

    def test_user_profile_DELETE(self):
        """Test whether a user can delete their profile"""
        self.client.login(username="TestUser", password="TestUser123!")
        user_profile_url_user_name = reverse('User Profile', args=['TestUser'])
        response = self.client.delete(user_profile_url_user_name)
        self.assertEquals(response.status_code, 302)
