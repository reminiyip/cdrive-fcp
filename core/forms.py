from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CardPayment, UserProfile, User
from .utils.credit_card_fields import CreditCardField, ExpiryDateField, VerificationValueField

class PaymentForm(forms.ModelForm):
	name_on_card = forms.CharField(max_length=50, required=True)
	card_number = CreditCardField(required=True)
	expiration_date = ExpiryDateField(required=True)
	security_code = VerificationValueField(required=True)

	class Meta:
		model = CardPayment
		fields = ('name_on_card', 'card_number', 'expiration_date', 'security_code', )

class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2',)

class UserEmailForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('email',)

class UserProfileForm(forms.ModelForm):	
	class Meta:
		model = UserProfile
		fields = ('on_screen_name', 'avatar_image',)
