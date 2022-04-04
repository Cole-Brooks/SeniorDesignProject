from .models import Car
from django import forms
from administrators.models import ParkingLot


class RegisterCarForm(forms.ModelForm):
    """Login form to for adding a car"""

    parking = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        fields = ('make', 'model', 'license_plate_number', 'state', 'parking')


class ParkingLotMembership(forms.Form):
    """Form for customer to join parking lots as members"""
    parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.HiddenInput)


