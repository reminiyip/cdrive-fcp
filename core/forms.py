from django import forms

from .models import CardPayment

class PaymentForm(forms.ModelForm):

	class Meta:
		model = CardPayment
		fields = ('card_number', 'expiration_date', 'security_code', )