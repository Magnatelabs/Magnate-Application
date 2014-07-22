from django import forms
from share.models import EmailShareModel
from django.utils.safestring import mark_safe


class EmailShareModelForm(forms.Form):
    share_email_list = forms.CharField(max_length=750)
    share_email_content = forms.CharField(max_length=750)

    def __init__(self, *args, **kwargs):
        super(EmailShareModelForm, self).__init__(*args, **kwargs)
        self.fields['share_email_list'].widget.attrs['id'] = 'super_first'
