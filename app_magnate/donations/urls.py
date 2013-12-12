from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from donations import views 

from billing import get_integration
from  donations.views import DonationBilling


#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns("",
  url(r"^donations/home$", "donations.views.donation_index", name="donations_home"),
  url(r"^donations/add$", "donations.views.donation_add", name="donations_add"),
  url(r"^donations/billing$", "donations.views.enter_billing_info", name="donations_billing"),
#  url(r"^donations/finalize_order$", "donations.views.DonationBilling", name="donations_finalize"),
  url(r"^donations/finalize_order$", DonationBilling.as_view(), name="donations_finalize"),
  url(r"^donations/confirmation$", "donations.views.donation_confirmation", name="donations_confirmation"),
  url(r"^donations/finalize_order$", "donations.views.donation_orderpay", name="donations_pay"),
  url(r"^fundstart/tierselection$", "donations.views.donation_tiers", name="donations_tiers"),
)

int_obj = get_integration("authorize_net_dpm")
urlpatterns += patterns('',
   (r'^authorize_net/', include(int_obj.urls)),
)
