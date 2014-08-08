from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime 

#imports to recognize django messages
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

#imports to recognize forms 
from share.forms import EmailShareModelForm
from share.models import EmailShareModel

#import to recognize class based view
from django.views.generic.edit import FormView


class share_index(FormView):
#    import pdb #(test for checking each process)
#    pdb.set_trace()
     
    template_name = 'share/_share_lightbox.html'
    form_class = EmailShareModelForm
    redirect_field_name = "next"
    messages = {
        "survey_added": {
            "level": messages.SUCCESS,
            "text": _(u"Your friends will re information was successfully submitted.")
        },
        "input_error": {
            "level": messages.ERROR,
            "text": _(u"Your information was not entered correctly. Please try again.")
        }
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Process the data in form.cleaned_data
            entry = EmailShareModel()
            entry.share_email_list = form.data['share_email_list']
            entry.share_email_content = form.data['share_email_content']
            entry.created = datetime.datetime.now()
            entry.user = request.user
            entry.save()
	    messages.add_message(
                self.request,
                self.messages["survey_added"]["level"],
                self.messages["survey_added"]["text"]
            )
            return redirect('dashboard') # Redirect after POST    
#            return redirect('confirm_questions') # Redirect after POST
        else:
            messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            )
            print 'DEBUG: form is not valid!!!', form.errors