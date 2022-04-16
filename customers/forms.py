from .models import Car
from django import forms
from administrators.models import ParkingLot
from django.utils.html import format_html
from paypal.standard.forms import PayPalPaymentsForm


class RegisterCarForm(forms.ModelForm):
    """Login form to for adding a car"""

    parking = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}))

    class Meta:
        model = Car
        fields = ('make', 'model', 'license_plate_number', 'state',)
        
        
class UpdateParkingCarForm(forms.ModelForm):
    """Login form to for adding a car"""

    parking = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.Select(
        attrs={'class': 'form-control'}))
    
    class Meta:
        model = Car
        fields = ('parking',)


class ParkingLotMembership(forms.Form):
    """Form for customer to join parking lots as members"""
    parking_lot = forms.ModelChoiceField(queryset=ParkingLot.objects.all(), widget=forms.HiddenInput)


class CustomPayPalPaymentsForm(PayPalPaymentsForm):

    def render(self, *args, **kwargs):
        if not args and not kwargs:
            return format_html(
                """<form action="{0}" method="post">{1} <input type="image" src="{2}" 
                class="btn btn-warning" name="submit" alt="Pay with PayPal or Debit (Credit) Card"/>
                </form>""",
                self.get_login_url(),
                self.as_p(),
                ''
            )
        else:
            return super().render(*args, **kwargs)
