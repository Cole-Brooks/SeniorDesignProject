from django.test import TestCase
from ..models import User
from ..forms import RegistrationForm, LoginForm, UserProfileForm, UserForm


# Create your tests here.
class TestLogin(TestCase):
    """Test forms related to the user"""

    def test_login_form(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username:')
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Password:')

    def test_registration_form_help_text(self):
        form = RegistrationForm()
        self.assertEqual(form.fields['email'].help_text, "We don't share your email.")
