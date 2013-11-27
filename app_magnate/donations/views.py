from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.template import RequestContext
import datetime


from billing import get_integration

#imports to recognize django messages
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

#import to recognize class based view
from django.views.generic.edit import FormView

#imports to recognize forms 
from .forms import BillingInfoForm
from .models import BillingInfo
from .utils import total_donation_amount



def donation_index(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)
    tda=total_donation_amount(request.user)
    user_has_donation = (tda > 0)

    return render(request, 'donations/donations_home.html', {'user_has_donation': user_has_donation, 'total_donation_amount': tda})

def donation_tiers(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'donations/donations_tiers.html')

def donation_add(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'donations/donations_add.html')

class DonationBilling(FormView):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    template_name = 'donations/donations_billing.html'
    form_class = BillingInfoForm
    success_url='/thanks/'
    redirect_field_name = "next"
    dumb_messages = {
        "survey_added": {
            "level": messages.SUCCESS,
            "text": _(u"Your information was successfully submitted.")
        },
        "input_error": {
            "level": messages.ERROR,
            "text": _(u"Your information was not entered correctly. Please try again.")
        }
    }

    def is_valid(self, form):
        print 'IS_VALID'
        return True

    def get(self, request, *args, **kwargs):
        print 'GET!!!'
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print 'POST!!!'
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            entry = BillingInfo()
            entry.first_name = form.data['first_name']
            entry.last_name = form.data['last_name']
            entry.address = form.data['address']
            entry.city = form.data['city']
            entry.zip = form.data['zipcode']
            entry.country = form.data['country']
            entry.save()
            dumb_messages.add_message(
                self.request,
                self.messages["survey_added"]["level"],
                self.messages["survey_added"]["text"]
            )
    
            return redirect('donations_pay') # Redirect after POST
        else:
            dumb_messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            )
            print 'DEBUG: form is not valid!!!', form.errors

#def confirmation_index(request):
#    return render(request, 'donations/donations_pay.html')


def donation_confirmation(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'donations/donations_confirmation.html')

def donation_orderpay(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    int_obj = get_integration("authorize_net_dpm")
    fields = {'x_amount': 1,
          'x_fp_sequence': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
          'x_fp_timestamp': datetime.datetime.utcnow().strftime('%s'),
          'x_recurring_bill': 'F',
          'x_relay_url': request.build_absolute_uri(reverse("authorize_net_notify_handler")),
          'x_cust_id': request.user,
        }
    int_obj.add_fields(fields)
    return render_to_response("donations/donations_orderpay.html",
                             {"adp": int_obj},
                             context_instance=RequestContext(request))
