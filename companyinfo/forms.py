from django import forms
from companyinfo.models import MediaUpdates

class MediaUpdatesForm(forms.Form):

    signup_email = forms.EmailField()
    name = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(MediaUpdatesForm, self).__init__(*args, **kwargs)
        self.fields["signup_email"].widget.attrs["placeholder"] = "Email"
        self.fields["signup_email"].label = ""
        self.fields["name"].widget.attrs["placeholder"] = "Name"
        self.fields["name"].label = ""
