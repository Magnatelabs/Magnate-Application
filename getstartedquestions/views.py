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
from getstartedquestions.forms import QuestionListForm
from getstartedquestions.models import QuestionList

#import to recognize class based view
from django.views.generic.edit import FormView

from forum.models.user import User as ForumUser
from forum.utils.mail import send_template_email


class survey_index(FormView):
#    import pdb #(test for checking each process)
#    pdb.set_trace()
     
    template_name = 'getstartedquestions/questionnaire.html'
    form_class = QuestionListForm
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
        form = self.form_class(initial={'waitinglistemail': request.GET.get('email')})#(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            entry = QuestionList()
            entry.first_name = form.data['first_name']
            entry.last_name = form.data['last_name']
            entry.waitinglistemail = form.data['waitinglistemail']
            entry.sex = form.data['sex']
            entry.industry_preference = form.data['industry_preference']
            entry.funding_knowledge = form.data['funding_knowledge']
            entry.site_rec = form.data['site_rec']
            entry.income = form.data['income']
            entry.funding_preference = form.data['funding_preference']
            entry.created = datetime.datetime.now()

            #s = form.data['dob']
            #Convert date from 05/29/1986 to 1986--05--29
            #entry.dob = s[-4:] + '-' + s[:2] + '-' + s[3:5]
            entry.dob = form.cleaned_data['dob']
            entry.save()
	    messages.add_message(
                self.request,
                self.messages["survey_added"]["level"],
                self.messages["survey_added"]["text"]
            )
    
            user = ForumUser(username='newuser', email='a@mailinator.com')
            #send_template_email([user], "notifications/alphasignupcomplete.html", {"survey": entry})

            return redirect('confirm_questions') # Redirect after POST
        else:
            messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            )

            print 'DEBUG: form is not valid!!!', form.errors
            return render(request, self.template_name, {'form': form})


def confirmation_index(request):
    return render(request, 'getstartedquestions/confirmation.html')
