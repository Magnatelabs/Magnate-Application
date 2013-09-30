from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

#imports to recognize django messages
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from dashboard.models import SpotlightRequest
from dashboard.forms import SpotlightRequestForm

#import to recognize class based view
from django.views.generic.edit import FormView




def dashboard_index(request):
    if not request.user.is_authenticated():
        return redirect('/account/login/?next=%s' % request.path)

    return render(request, 'dashboard/dashboard_main.html')



class dashboard_spotlight_request(FormView):
#    import pdb #(test for checking each process)
#    pdb.set_trace()
     
    template_name = 'dashboard/dashboard_main.html'
    form_class = SpotlightRequestForm
    redirect_field_name = "next"
    messages = {
        "spotlight_added": {
            "level": messages.SUCCESS,
            "text": _(u"The required information was submitted successfully.")
        },
        "input_error": {
            "level": messages.ERROR,
            "text": _(u"The required information was not entered correctly. Please try again.")
        }
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            entry = SpotlightRequest()
            entry.company = form.data['company']
            entry.platform = form.data['platform']
            entry.industry = form.data['industry']
            entry.deadline = form.data['deadline']
            entry.reason = form.data['reason']
            entry.amount = form.data['amount']
            entry.request_created = datetime.datetime.now()
            s = form.data['deadline']
            entry.deadline = s[-4:] + '-' + s[:2] + '-' + s[3:5]
            # Convert date from 05/29/1986 to 1986--05--29   
            user = request.user
            # Request and create an instance of current user.
            entry.user = user
            entry.save()
            messages.add_message(
                self.request,
                self.messages["spotlight_added"]["level"],
                self.messages["spotlight_added"]["text"]
            )

            return redirect('confirm_dashboard') # Redirect after POST
        else:
            messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            )
            print 'DEBUG: form is not valid!!!', form.errors


def dash_confirm_index(request):
    return render(request, 'dashboard/dashboard_confirm.html')
