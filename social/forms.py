from django import forms
from social.models import FeedbackModel
from django.utils.safestring import mark_safe


# django knows to look for each input field, 
# as long the form subclass defines the fields
# in the same order as the model.

class FeedbackModelForm(forms.Form):
    
    feedback_paragraph = forms.CharField(max_length=750)

    def __init__(self, *args, **kwargs):
        super(FeedbackModelForm, self).__init__(*args, **kwargs)
        self.fields['feedback_paragraph'].widget.attrs['id'] = 'super_first'


