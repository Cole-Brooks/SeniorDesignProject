from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import ParkingLot
from localflavor.us.forms import USZipCodeField
from localflavor.us.us_states import STATE_CHOICES


class RegisterParkingForm(forms.ModelForm):
    """Login form to for adding a parking"""

    zip_code = USZipCodeField()
    overview = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Add any details or a quick summary you would like customers to know about your parking lot',
            "rows": 7, "cols": 20}))
    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    business_email = forms.EmailField(label='Business email', min_length=5, required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'Enter your business PayPal account email', 'class': 'form-control'}),
                                      help_text="We don't share your email, we use it for payments purposes.")
    fee_per_hour = forms.DecimalField(required=True, max_digits=8, min_value=0.0, initial=1.0)
    max_overdue = forms.DecimalField(required=True, max_digits=8, min_value=0.0, initial=0.0)

    class Meta:
        model = ParkingLot
        fields = ('parking_name', 'overview', 'street_address', 'city', 'state', 'zip_code', 'phone_number',
                  'business_email', 'capacities', 'free_spots', 'fee_per_hour',
                  'max_overdue')


class SearchParking(forms.ModelForm):
    """Field for searching Field"""
    key = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search parking lots by name, city or zip code', 'class': 'form-control'}))
