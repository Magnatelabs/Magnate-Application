from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.template import RequestContext
import datetime
import time
import logging

from billing import get_integration

#imports to recognize django messages
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

#import to recognize class based view
from django.views.generic.edit import FormView

#imports to recognize forms 
from .forms import BillingInfoForm
from .models import BillingInfo, MagnateFund, PortfolioCompany
from .utils import total_donation_amount
from bonus_awards.utils import total_bonus_amount

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

#@login_required                                                                                
def fundpage_index(request):
#    if not request.user.is_authenticated():                                                   #        return redirect('/donations/user/?next=%s' % request.path)                             
    tda=total_donation_amount(request.user)
    user_has_donation = (tda > 0)
    tba=total_bonus_amount(request.user)
    gt= tda+tba

    funds = MagnateFund.objects.all()
    portfolio = PortfolioCompany.objects.all()


    return render(request, 'donations/fund_homepage.html', {'funds': funds, 'portfolio': portfolio, 'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt })
#    return render(request, 'donations/fund_homepage.html')


#@login_required
def donation_index(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)
    tda=total_donation_amount(request.user)
    user_has_donation = (tda > 0)
    tba=total_bonus_amount(request.user)
    gt= tda+tba

    return render(request, 'donations/donations_home.html', {'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt })

#@login_required
def donation_add(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'donations/donations_add.html')

def enter_billing_info(request, form=None):
    return render(request, 'donations/donations_billing.html', {
        'amount': request.POST['amount'], 'form': form})


class DonationBilling(FormView):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    template_name = 'donations/donations_billing.html'
    form_class = BillingInfoForm
#    success_url = reverse_lazy('donations_pay')
    redirect_field_name = "next"
    messages = {
        "survey_added": {
            "level": messages.SUCCESS,
            "text": _(u"Your billing information was successfully saved.")
        },
        "input_error": {
            "level": messages.ERROR,
            "text": _(u"Your information was not entered correctly. Please try again.")
        }
    }

#    def is_valid(self, form):
#        print 'IS_VALID'
#        return True

#    @login_required
    def get(self, request, *args, **kwargs):
        # This is actually never used, as the previous page donations_add is doing POST
        print 'GET!!!'
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

#    @login_required
    def post(self, request, *args, **kwargs):
        if 'coming_from_donations_add' in request.POST:
            # display the form for the first time
            form = self.form_class(initial=self.initial)
            return enter_billing_info(request, form)

        print 'POST!!!'
#        import pdb #(test for checking each process)
#        pdb.set_trace()
        form = self.form_class(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            entry = BillingInfo()
#            entry.user = form.data['user']
            entry.first_name = form.data['first_name']
            entry.last_name = form.data['last_name']
            entry.address = form.data['address']
            entry.city = form.data['city']
            entry.zip = form.data['zipcode']
            entry.country = form.data['country']
            entry.amount = float(form.data['amount'])
            entry.save()
#            user_id = request.user.id
#            form.instance.user = request.user
#            userid = entry.save(commit=False)
#            userid.user = request.user
#            userid.save()

            messages.add_message(
                self.request,
                self.messages["survey_added"]["level"],
                self.messages["survey_added"]["text"]
            )

            return donation_orderpay(request, entry)
#            return redirect(request, 'donations/donations_orderpay.html', {'amount': request.POST['amount']}) # Redirect after POST
#            return render(request, 'donations/donations_orderpay.html')
        else:
            messages.add_message(
                self.request,
                self.messages["input_error"]["level"],
                self.messages["input_error"]["text"]
            ) 
            # monkey patch: passing the amount back to itself
            return render(request, self.template_name, {'form': form, 'amount': form.data['amount']})
            print 'DEBUG: form is not valid!!!', form.errors

#def confirmation_index(request):
#    return render(request, 'donations/donations_pay.html')

#@login_required
def donation_confirmation(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'donations/donations_confirmation.html')


#@login_required
@require_http_methods(["POST"])
def donation_orderpay(request, entry):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    donation_amount = request.POST['amount']
    objective = request.POST.get('objective', None)
#    donation_amount = request.POST['donation_amount']
    int_obj = get_integration("authorize_net_dpm")
    fields = {'x_amount': donation_amount,
          'x_fp_sequence': datetime.datetime.now().strftime('%Y%m%d%H%M%S'), # any identifier for the transaction
          'x_fp_timestamp': str(int(time.time())), # the timestamp when x_fp_sequence was generated
          'x_recurring_bill': 'F',
          'x_relay_url': request.build_absolute_uri(reverse("authorize_net_notify_handler")),
          'x_cust_id': request.user,
          'x_extra_data': '{}',
          'x_first_name': entry.first_name,
          'x_last_name': entry.last_name,
          'x_zip': entry.zip,
          'x_address': entry.address,
          'x_city': entry.city,
          'x_country': entry.country,
        }
    if objective is not None:
        fields['x_extra_data'] = '{ "objective": %s }' % objective
    int_obj.add_fields(fields)

    logging.info("User '%s' is prepared to donate. Entering payment info..." % (request.user))
    return render_to_response("donations/donations_orderpay.html",
                             {"adp": int_obj,
                              "amount": donation_amount,
                              "objective": objective},
                             context_instance=RequestContext(request))

#@login_required
def contribution_history(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)
    tda=total_donation_amount(request.user)
    user_has_donation = (tda > 0)
    tba=total_bonus_amount(request.user)
    gt= tda+tba

    return render(request, 'donations/contribution_history.html', {'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt })
