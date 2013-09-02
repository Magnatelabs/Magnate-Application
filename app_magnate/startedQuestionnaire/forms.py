from django import forms
from startedQuestionnaire.models import QuestionList
#do I need to import the model?


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.

class QuestionListForm(forms.Form):

    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    sex = forms.CharField(max_length=200)
    dob = forms.DateField(input_formats=['%m/%d/%Y',], required=False, widget=forms.DateInput(format = '%m/%d/%Y') )
    funding_knowledge = forms.CharField(max_length=200)
    income = forms.IntegerField()
    funding_preference = forms.CharField(max_length=200)
    industry_preference = forms.CharField(max_length=200)
    site_rec = forms.CharField(max_length=200)


# def __init__(self, *args, **kwargs):
#        super(WaitingListEntryForm, self).__init__(*args, **kwargs)
#        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
#        self.fields["email"].label = ""
