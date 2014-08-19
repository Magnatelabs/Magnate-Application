from django import forms
from .models import StudyModel
from django.utils.safestring import mark_safe

INDUSTRY_CHOICES = (('mobile', 'Mobile'), ('e-commerce', 'E-commerce'), ('social-network', 'Social Network'), ('fitness', 'Fitness'), ('other', 'Other'))

class StudyModelForm(forms.Form):
    entity = forms.CharField(max_length=255)
    entity_url = forms.URLField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, max_length=750)
    industry = forms.ChoiceField(widget=forms.Select, choices=INDUSTRY_CHOICES)
    docfile = forms.FileField(label='Additional Material', required=False)
 
    def __init__(self, *args, **kwargs):
        super(StudyModelForm, self).__init__(*args, **kwargs)
        self.fields['entity'].widget.attrs['id'] = 'super_first'
