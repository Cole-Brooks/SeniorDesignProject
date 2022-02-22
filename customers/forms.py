from .models import Car
from django import forms
from administrators.models import ParkingLot


class RegisterCarForm(forms.Form):
    """Login form to for adding a car"""

    class Meta:
        model = Car
        fields = ('make', 'model', 'license_plate_number', 'state')


class ParkingLotMembership(forms.Form):
    """Form for customer to join parking lots as members"""
    parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.HiddenInput)
