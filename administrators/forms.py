from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import ParkingLot
from localflavor.us.forms import USZipCodeField


class RegisterParkingForm(forms.ModelForm):
    """Login form to for adding a parking"""
    zip_code = USZipCodeField()
    class Meta:
        model = ParkingLot
        fields = ('administrator', 'parking_name', 'street_address', 'city', 'state', 'zip_code', 'phone',
                  'business_email', 'customer', 'capacities', 'free_spots', 'overview', 'fee_per_hour', 'max_overdue')



