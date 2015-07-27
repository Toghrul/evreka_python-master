from django import forms
from homepage.models import ContactModel


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactModel