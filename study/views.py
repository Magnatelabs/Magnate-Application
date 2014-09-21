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
from .forms import StudyModelForm
from .models import ProposeCompanyAction

#import to recognize class based view
from django.views.generic.edit import FormView


class study_index(FormView):
#    import pdb #(test for checking each process)
#    pdb.set_trace()
     
    template_name = 'study/initial_submit.html'
    form_class = StudyModelForm
    redirect_field_name = "next"
    messages = {
        "survey_added": {
            "level": messages.SUCCESS,
            "text": _(u"Your information was successfully submitted.")
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
            action = ProposeCompanyAction(user=request.user, ip=request.META['REMOTE_ADDR']).save(dict(form=form, docfile=request.FILES['docfile'] if 'docifle' in request.FILES else None))
            # Process the data in form.cleaned_data
#            entry = StudyModel()
#            entry.entity = form.data['entity']
#            entry.entity_url = form.data['entity_url']
#            entry.description = form.data['description']
#            entry.industry = form.data['industry']
#            entry.created = datetime.datetime.now()
#            if 'docfile' in request.FILES:
#              entry.docfile = request.FILES['docfile']
#            if request.user.is_authenticated():
#              entry.user = request.user
#            entry.save()
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
            return render(request, self.template_name, {'form': form})


def submit_completed(request):
    return render(request, 'study/confirmation.html')
