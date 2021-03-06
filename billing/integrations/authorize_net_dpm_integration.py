from billing import Integration, IntegrationNotConfigured
from billing.forms.authorize_net_forms import AuthorizeNetDPMForm, AuthorizeNetDPMFormCheck
from billing.signals import transaction_was_successful, transaction_was_unsuccessful
from django.conf import settings
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
import hashlib
import hmac
import urllib

import logging
logger=logging.getLogger(__name__)

csrf_exempt_m = method_decorator(csrf_exempt)
require_POST_m = method_decorator(require_POST)


class AuthorizeNetDpmIntegration(Integration):
    display_name = "Authorize.Net Direct Post Method"
    template = "billing/authorize_net_dpm.html"

    def __init__(self):
        super(AuthorizeNetDpmIntegration, self).__init__()
        merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("authorize_net"):
            raise IntegrationNotConfigured("The '%s' integration is not correctly "
                                           "configured." % self.display_name)
        self.authorize_net_settings = merchant_settings["authorize_net"]

    def form_class(self):
        return AuthorizeNetDPMForm
#        return AuthorizeNetDPMFormCheck

    def generate_form(self):
        transaction_key = self.authorize_net_settings["TRANSACTION_KEY"]
        login_id = self.authorize_net_settings["LOGIN_ID"]

        initial_data = self.fields
        x_fp_hash = hmac.new(transaction_key, "%s^%s^%s^%s^" % (login_id,
                                                               initial_data['x_fp_sequence'],
                                                               initial_data['x_fp_timestamp'],
                                                               initial_data['x_amount']),
                             hashlib.md5)
        initial_data.update({'x_login': login_id,
                             'x_fp_hash': x_fp_hash.hexdigest()})
        form = self.form_class()(initial=initial_data)
        return form

    @property
    def service_url(self):
        if self.test_mode:
#            return "http://localhost:9000"
             return "https://test.authorize.net/gateway/transact.dll"
        return "https://secure.authorize.net/gateway/transact.dll"

    def verify_response(self, request):
        data = request.POST.copy()
        md5_hash = self.authorize_net_settings["MD5_HASH"]
        login_id = self.authorize_net_settings["LOGIN_ID"]
        hash_str = "%s%s%s%s" % (md5_hash, login_id,
                                 data.get("x_trans_id", ""),
                                 data.get("x_amount", ""))
        if not 'x_MD5_Hash' in data:
            return False
        return hashlib.md5(hash_str).hexdigest() == data.get("x_MD5_Hash").lower()

    @csrf_exempt_m
    @require_POST_m
    def authorizenet_notify_handler(self, request):
        response_from_authorize_net = self.verify_response(request)
        if not response_from_authorize_net:
            print "LOG WARN: Returning HttpResponseForbidden, the response was not from Authorize.Net. MD5 checksum mismatch. Make sure MD5_HASH in Django settings matches the MD5 key set on the Authorize.Net server"
            return HttpResponseForbidden() # FIXED BUG; was return HttpResponseForbidden
        result = request.POST["x_response_reason_text"]
        extra_data = request.POST.get('x_extra_data', '{}')
        import json
        extra_data = json.loads(extra_data)
        if request.POST['x_response_code'] == '1':
            transaction_was_successful.send(sender=self,
                                             request=request)
            redirect_url = "%s?%s" % (request.build_absolute_uri(reverse("authorize_net_success_handler")),
                                     urllib.urlencode(dict({"response": result,
                                                       "transaction_id": request.POST["x_trans_id"]}.items() + extra_data.items())))
            return render_to_response("billing/authorize_net_relay_snippet.html",
                                      {"redirect_url": redirect_url})
        print "WARN: Authorize.Net transaction rejected. x_response_code=%s, x_response_reason_code=%s" % (request.POST['x_response_code'], request.POST['x_response_reason_code'])
         # Check http://www.authorize.net/support/merchant/Transaction_Response/Response_Reason_Codes_and_Response_Reason_Text.htm for codes
        redirect_url = "%s?%s" % (request.build_absolute_uri(reverse("donations_add")),
                                 urllib.urlencode(dict({"response": result}.items() + extra_data.items())))
        transaction_was_unsuccessful.send(sender=self,
                                          request=request)
        return render_to_response("billing/authorize_net_relay_snippet.html",
                                  {"redirect_url": redirect_url})

    def authorize_net_success_handler(self, request):
        response = request.GET
            
        objective=request.GET.get('objective', None)
        if objective is not None:
            from rewards.models import FundraisingAgenda
            try:
              objective=FundraisingAgenda.objects.get(pk=int(objective))
            except:
              logging.exception("Contributed donation to nonexistent objective %s" % request.GET['objective'])
              objective = None
        return render_to_response("billing/authorize_net_success.html",
                                  {"response": response, "objective": objective},
                                  context_instance=RequestContext(request))

    def authorize_net_failure_handler(self, request):
        response = request.GET
        return render_to_response("billing/authorize_net_failure.html",
                                  {"response": response},
                                  context_instance=RequestContext(request))

    def get_urls(self):
        urlpatterns = patterns('',
           url('^authorize_net-notify-handler/$', self.authorizenet_notify_handler, name="authorize_net_notify_handler"),
           url('^authorize_net-success-handler/$', self.authorize_net_success_handler, name="authorize_net_success_handler"),
           url('^authorize_net-failure-handler/$', self.authorize_net_failure_handler, name="authorize_net_failure_handler"),)
        return urlpatterns
