from django import forms
from .models import StudyModel
from django.utils.safestring import mark_safe


class StudyModelForm(forms.Form):
    entity = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    analysis = forms.CharField(max_length=750)
    docfile = forms.FileField(label='Select a file',)
 
    def __init__(self, *args, **kwargs):
        super(StudyModelForm, self).__init__(*args, **kwargs)
        self.fields['entity'].widget.attrs['id'] = 'super_first'
