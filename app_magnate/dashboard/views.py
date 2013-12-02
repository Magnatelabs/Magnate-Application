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

from donations.utils import total_donation_amount, all_donations_by_user, all_badges_for_user




import zinnia
from zinnia.views.archives import EntryIndex

def dashboard_index(request):
    if not request.user.is_authenticated():
        return redirect('/account/login/?next=%s' % request.path)

    feed=all_donations_by_user(request.user)
    tda = total_donation_amount(request.user)
    user_has_donation = (tda > 0)

    user_badges = all_badges_for_user(request.user)
 

    return EntryIndex.as_view()(request, 'dashboard/dashboard_main.html', {'user_has_donation': True} )

#    return render(request, 'dashboard/dashboard_main.html', {'user_has_donation': user_has_donation, 'feed': feed, 'total_donation_amount': tda, 'user_badges': user_badges})



class DashboardView(zinnia.views.archives.EntryIndex):

    # Overloading get_context_data so we can pass extra variables to the template.
    # See https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-display/
    def get_context_data(self, **kwargs):

        # Get current context
        context = super(DashboardView, self).get_context_data(**kwargs)

        # Add more variables to the context so we can render the dashboard view.
        # Add any specific information for the user who is currently logged in.
        assert self.request.user.is_authenticated(), "No user is logged in. Why are we trying to render a page? The user should have been redirected to a login page. In fact, all views in %s should be decorated with @login_required." % (self.__class__.__name__)
        username = self.request.user               

        amount = total_donation_amount(username)
        context['user_has_donation'] = (amount > 0)
        context['total_donation_amount'] = str(amount)
        context['feed'] = all_donations_by_user(username)
        context['user_badges'] = all_badges_for_user(username)
        return context


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
