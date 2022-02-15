from django.test import TestCase
from ..models import User


# Create your tests here.
class TestUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        username = "test4"
        first_name = "Kevin"
        last_name = "Hurt"
        email = "test@gmail.com"
        password = "lavieestbelle"

        # Set up object used by test methods
        User.objects.create(username=username, first_name=first_name, last_name=last_name,
                            email=email, password=password)

    def test_string_method(self):
        # Create user object to test
        user = User.objects.get(id=1)
        # construct the expected string
        expected_string = user.first_name + " " + user.last_name
        # Compare the value to the expected result
        self.assertEqual(user.__str__(), expected_string)

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')
        
    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')
        
    def test_last_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')
        
    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')
        
    def test_password_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        self.assertEqual(field_label, 'password')
        

