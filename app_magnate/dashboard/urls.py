from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from dashboard import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^dashboard/$", "dashboard.views.dashboard_index", name="dashboard"),
  url(r"^dashboard/spotlightrequest/$", "dashboard.views.dashboard_spotlight_request", name="spotlight_request"),
)
