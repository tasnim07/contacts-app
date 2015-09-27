from django import forms
from django.core.exceptions import ValidationError
from contacts.models import Contact, Address
from django.forms.models import inlineformset_factory

class ContactForm(forms.ModelForm):

	confirm_email = forms.EmailField(label="Confirm email", required=True)

	class Meta:
		model = Contact
		fields = ("first_name", "last_name", "email", "confirm_email",)


	def __init__(self, *args, **kwargs):
		if kwargs.get('instance'):
				# INFO: it's only for the edit contact
			email = kwargs['instance'].email
			kwargs.setdefault('initial', {})['confirm_email'] = email

		return super(ContactForm, self).__init__(*args, **kwargs)

	def clean(self):
		if (self.cleaned_data.get('email') != self.cleaned_data.get('confirm_email')):
			raise ValidationError("Email addresses must match.")

		return self.cleaned_data

ContactAddressFormSet = inlineformset_factory(Contact, Address, fields=('__all__'))