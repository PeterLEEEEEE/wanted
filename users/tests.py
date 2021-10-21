import json 
from django.test import TestCase, Client
from users.models import User


# Create your tests here.

class SignUpViewTest(TestCase):
    def test_signup_success(self):
        client = Client()

        user = {
            "name": "peter",
            "email": "dissgo12@gmail.com",
            "password": "dlangus1234!"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE':'SUCCESSFULLY REGISTERED'})
    
    def test_signup_keyerror(self):
        client = Client()

        user = {
            "email": "dissgo12@gmail.com",
            "password": "dlangus1234!"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'KEY_ERROR'})

    def test_signup_valueerror(self):
        client = Client()

        response = client.post("/users/register")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'VALUE_ERROR'})
    
    def test_signup_wrong_name_format(self):
        client = Client()

        user = {
            "name"    : "p",
            "email"   : "dissgo12@gmail.com",
            "password": "dlangus1234!"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'WRONG NAME FORMAT'})

    def test_signup_wrong_email_format(self):
        client = Client()

        user = {
            "name"    : "peter",
            "email"   : "dissgo12@gmail.o",
            "password": "dlangus1234!"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'WRONG EMAIL FORMAT'})
    
    def test_signup_wrong_password_format(self):
        client = Client()

        user = {
            "name"    : "peter",
            "email"   : "dissgo12@gmail.com",
            "password": "dlangus1234"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE' : 'WRONG PASSWORD FORMAT'})
    
    def setUp(self):
        User.objects.create(
            name     = "peter",
            email    = "dissgogo@gmail.com",
            password = "dlangus1234^"
        )

    def tearDown(self):
        User.objects.all().delete()
    
    def test_signup_email_already_exists(self):
        client = Client()

        user = {
            "name"    : "kim",
            "email"   : "dissgogo@gmail.com",
            "password": "dlangus1234^"
        }

        response = client.post("/users/register", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'MESSAGE':'EMAIL ALREADY EXISTS'})
