from django import forms
from .models import EmailShareModel
from django.utils.safestring import mark_safe


class EmailShareModelForm(forms.Form):
    share_email_list = forms.CharField(max_length=750)
    share_email_content = forms.CharField(max_length=750)

    def __init__(self, *args, **kwargs):
        super(StudyModelForm, self).__init__(*args, **kwargs)
        self.fields['entity'].widget.attrs['id'] = 'super_first'
