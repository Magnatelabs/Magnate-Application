from django import forms
from dashboard.models import SpotlightRequest


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.

class SpotlightRequestForm(forms.Form):

    company = forms.CharField(max_length=200)
    platform = forms.CharField(max_length=200)
    industry = forms.CharField(max_length=200)
    deadline = forms.DateField(input_formats=['%m/%d/%Y',], required=False, widget=forms.DateInput(format = '%m/%d/%Y') )
    reason = forms.CharField(max_length=200)
    amount = forms.CharField(max_length=100)


# def __init__(self, *args, **kwargs):
#        super(WaitingListEntryForm, self).__init__(*args, **kwargs)
#        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
#        self.fields["email"].label = ""
