from django import forms
"""Create django forms"""


class CreateBusinessForm(forms.Form):
    business_name = forms.CharField(max_length=100)
    business_type = forms.CharField(max_length=100)
    description = forms.CharField(max_length=5000)
    location = forms.CharField(max_length=50)
    email_contact = forms.CharField(max_length=100)
    phone_contact = forms.CharField(max_length=100)
