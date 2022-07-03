from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.authtoken.models import Token
# Create your tests here.

class RegisterTestCase(APITestCase):

    def test_register(self):
        data={
            "username":"testcase",
            "email":"testcase@e.com",
            "password":"NewPass@123",
            "confirm_password":"NewPass@123"
        }
        response =self.client.post(reverse('register'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='example',password='NewPassword@123')

    #login
    def test_login(self):
        data ={
            "username":"example",
            "password":"NewPassword@123"
        }
        response =self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #token 
    def test_logout(self):
        self.token= Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION ='Token '+self.token.key)
        response =self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)