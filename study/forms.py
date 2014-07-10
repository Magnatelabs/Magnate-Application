from django import forms
from .models import StudyModel
from django.utils.safestring import mark_safe


class StudyModelForm(forms.Form):
    entity = forms.CharField(max_length=255)
    entity_url = forms.CharField(max_length=255)
    description = forms.CharField(max_length=750)
    industry = forms.CharField(max_length=255)
    docfile = forms.FileField(label='Additional Material',)
 
    def __init__(self, *args, **kwargs):
        super(StudyModelForm, self).__init__(*args, **kwargs)
        self.fields['entity'].widget.attrs['id'] = 'super_first'
