from django import forms

from .models import CardPayment
from core.utils.credit_card_fields import CreditCardField, ExpiryDateField, VerificationValueField

class PaymentForm(forms.ModelForm):
	name_on_card = forms.CharField(max_length=50, required=True)
	card_number = CreditCardField(required=True)
	expiration_date = ExpiryDateField(required=True)
	security_code = VerificationValueField(required=True)

	class Meta:
		model = CardPayment
		fields = ('name_on_card', 'card_number', 'expiration_date', 'security_code', )