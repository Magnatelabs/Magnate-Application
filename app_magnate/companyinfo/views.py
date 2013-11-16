from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime

from companyinfo.models import MediaUpdates
from companyinfo.forms import MediaUpdatesForm


def aboutus_index(request):
    return render(request, 'companyinfo/aboutus.html')

def newsletter_signup(request):
    print "before pdb"
#    import pdb #(test for checking each process)
#    pdb.set_trace()
#    print "after pdb"
    if request.method == 'POST': # If the form has been submitted...
        form = MediaUpdatesForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            entry = MediaUpdates()
            entry.signup_email = form.data['signup_email']
            entry.name = form.data['name']
            entry.created = datetime.datetime.now()
            entry.save()
            return redirect('/') # Redirect after POST

        else:
            print "DEBUG: Form is not valid!", form.errors, "\n", request.POST, "\n", form

    else:
        form = MediaUpdates() # An unbound form

    return render(request, 'companyinfo/aboutus.html', {'request': request, #'email':request.POST['email'],
        'form': form,
    })
