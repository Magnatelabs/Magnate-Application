from django import forms
from donations.models import BillingInfo
from django.utils.safestring import mark_safe
import datetime


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.


class BillingInfoForm(forms.Form):

    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=200)
    zipcode = forms.CharField(max_length=20)
    country = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(BillingInfoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['id'] = 'super_first'


        

