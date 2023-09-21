from django.test import TestCase, Client
from users.views import Uzer
from businesses.views import Business
from django.urls import reverse
import json


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
        self.new_business_url = reverse('Register Business')

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
        self.assertEqual(response.status_code, 200)
        user = response.context['user']
        self.assertFalse(user.is_authenticated)
        self.assertContains(response, 'Wrong username or password. Try again')

    def test_user_signup_GET(self):
        """Tests if signup_url is accessible"""
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")

    def test_user_signup_POST_existing_email(self):
        """Post an existing user email during signup"""
        response = self.client.post(
            self.signup_url, {
                "first_name": "Test",
                "last_name": "User",
                "user_name": "TestUserTwo",
                "email": "testuser123@mail.com",
                "password": "TestUser123!"
            }
        )
        self.assertEqual(Uzer.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User email taken')

    def test_user_signup_POST_existing_username(self):
        """Post an existing username during signup"""
        response = self.client.post(
            self.signup_url, {
                "first_name": "Test",
                "last_name": "User",
                "user_name": "TestUser",
                "email": "uniqueemail@mail.com",
                "password": "TestUser123!"
            }
        )
        self.assertEqual(Uzer.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Username taken. Try another username')

    def test_user_signup_POST_invalid_username(self):
        """Post an invalid username during signup"""
        response = self.client.post(
            self.signup_url, {
                "first_name": "Test",
                "last_name": "User",
                "user_name": "login",
                "email": "uniqueemail@mail.com",
                "password": "TestUser123!"
            }
        )
        self.assertEqual(Uzer.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username')

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

    def test_user_profile_PUT(self):
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

    def test_user_profile_edit_PUT_used_mail(self):
        """Test that an existing email throws an error"""
        self.client.login(username="TestUser", password="TestUser123!")
        user_profile_url_user_name = reverse('User Profile', args=['TestUser'])
        response = self.client.post(user_profile_url_user_name, {
            "email": "testuser123@mail.com"
        })
        response_data = response.json()
        self.assertEqual(
            response_data, {"error": "User email already exists. Try another email"})
        updated_user = Uzer.objects.get(username='TestUser')
        self.assertEqual(updated_user.email, "testuser123@mail.com")

    def test_user_profile_DELETE(self):
        """Test whether a user can delete their profile"""
        self.client.login(username="TestUser", password="TestUser123!")
        user_profile_url_user_name = reverse('User Profile', args=['TestUser'])
        response = self.client.delete(user_profile_url_user_name)
        self.assertEquals(response.status_code, 302)
        self.assertEqual(Uzer.objects.count(), 0)

    def test_business_registration_GET(self):
        """Test whether the business registration site is
        inaccessible unless logged in"""
        response = self.client.get(self.new_business_url)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/user/login?next=/business/register')

    def test_business_registration_GET_logged_in(self):
        """Test whether the business registration site is available"""
        self.client.login(username="TestUser", password="TestUser123!")
        response = self.client.get(self.new_business_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "create_business.html")

    def test_business_registration_POST(self):
        """Test whether a user can post a business"""
        self.client.login(username="TestUser", password="TestUser123!")
        no_businesses = Business.objects.count()
        response = self.client.post(
            self.new_business_url, {
                "business_name": "Test Business",
                "business_type": "Testers",
                "description": "None-ya-biznuz",
                "location": "Test Location",
                "phone_contact": "729704553",
                "email_contact": "testbusiness@mail.com"
            }
        )
        one_businesses = Business.objects.count()
        self.assertEquals(no_businesses + 1, one_businesses)
        self.assertEquals(response.status_code, 302)
