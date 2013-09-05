from django import forms
from companyinfo.models import MediaUpdates

class MediaUpdatesForm(forms.Form):

    signup_email = forms.EmailField()
    name = forms.CharField(max_length=200)


# def __init__(self, *args, **kwargs):
#        super(WaitingListEntryForm, self).__init__(*args, **kwargs)
#        self.fields["email"].widget.attrs["placeholder"] = "your@email.com"
#        self.fields["email"].label = ""
