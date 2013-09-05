from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


from dashboard.models import SpotlightRequest
from dashboard.forms import SpotlightRequestForm


def dashboard_index(request):
    if not request.user.is_authenticated():
        return redirect('/account/login/?next=%s' % request.path)

    return render(request, 'dashboard/dashboard_main.html')



def dashboard_spotlight_request(request):
#    import pdb (test for checking each process)
#    pdb.set_trace()
    if request.method == 'POST': # If the form has been submitted...
        form = SpotlightRequestForm(request.POST) # A form bound to the POST data
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
            return redirect('/') # Redirect after POST
    else:
        form = SpotlightRequest() # An unbound form

    return render(request, 'dashboard/dashboard_main.html', {
        'form': form,
    })
