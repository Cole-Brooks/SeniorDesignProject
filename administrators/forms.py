from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import ParkingLot
from localflavor.us.forms import USZipCodeField
from localflavor.us.us_states import STATE_CHOICES


class RegisterParkingForm(forms.ModelForm):
    """Login form to for adding a parking"""
    
    zip_code = USZipCodeField()

    state = forms.ChoiceField(choices=STATE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ParkingLot
        fields = ('parking_name', 'overview', 'street_address', 'city', 'state', 'zip_code', 'phone',
                  'business_email', 'capacities', 'free_spots', 'fee_per_hour',
                  'max_overdue')


class SearchParking(forms.ModelForm):
    """Field for searching Field"""
    key = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search parking lots by name, city or zip code', 'class': 'form-control'}))
