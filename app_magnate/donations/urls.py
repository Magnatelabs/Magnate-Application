from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from donations import views 

from billing import get_integration
from  donations.views import DonationBilling

#for the FormView
#from dashboard.views import dashboard_spotlight_request 

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns("",
  url(r"^donations/home$", "donations.views.donation_index", name="donations_home"),
  url(r"^donations/add$", "donations.views.donation_add", name="donations_add"),
  url(r"^donations/billing$", DonationBilling.as_view(), name="donations_billing"),
  url(r"^donations/confirmation$", "donations.views.donation_confirmation", name="donations_confirmation"),
  url(r"^donations/finalize_order$", "donations.views.donation_orderpay", name="donations_pay"),
  url(r"^fundstart/tierselection$", "donations.views.donation_tiers", name="donations_tiers"),
)

int_obj = get_integration("authorize_net_dpm")
urlpatterns += patterns('',
   (r'^authorize_net/', include(int_obj.urls)),
)
