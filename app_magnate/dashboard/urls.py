from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from dashboard import views 

#for the FormView
from dashboard.views import dashboard_spotlight_request 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^dashboard/$", "dashboard.views.dashboard_index", name="dashboard"),
  url(r"^dashboard/spotlightrequest/$", dashboard_spotlight_request.as_view(), name="spotlight_request"),
url(r"^spotlight_confirm/$", "dashboard.views.dash_confirm_index", name="confirm_dashboard"),
#  url(r"^dashboard/spotlightrequest/$", "dashboard.views.dashboard_spotlight_request", name="spotlight_request"),
)
