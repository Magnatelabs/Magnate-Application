from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime 

from startedQuestionnaire.forms import QuestionListForm
from startedQuestionnaire.models import QuestionList

#def survey_index(request):
#    return render(request, 'questionnaire.html', {'request': request, 'email': request.POST['email'] })


def survey_index(request):
#    import pdb (test for checking each process)
#    pdb.set_trace()
    if request.method == 'POST': # If the form has been submitted...
        form = QuestionListForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            entry = QuestionList()
            entry.first_name = form.data['first_name']
            entry.last_name = form.data['last_name']
            entry.sex = form.data['sex']
            entry.dob = form.data['dob']
            entry.industry_preference = form.data['industry_preference']
            entry.funding_knowledge = form.data['funding_knowledge']
            entry.site_rec = form.data['site_rec']
            entry.income = form.data['income']
            entry.funding_preference = form.data['funding_preference']
            entry.created = datetime.datetime.now()
            s = form.data['dob']
            # Convert date from 05/29/1986 to 1986--05--29
            entry.dob = s[-4:] + '-' + s[:2] + '-' + s[3:5]
            entry.save()
            return redirect('/') # Redirect after POST
    else:
        form = QuestionList() # An unbound form

    return render(request, 'startedQuestionnaire/questionnaire.html', {
        'form': form,
    })
