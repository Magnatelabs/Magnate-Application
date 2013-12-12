from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from dashboard import views 

#for the FormView
from dashboard.views import dashboard_spotlight_request 
from dashboard.views import DashboardView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^dashboard/$", DashboardView.as_view(), name="dashboard"),
  url(r"^dashboard/spotlightrequest/$", dashboard_spotlight_request.as_view(), name="spotlight_request"),
url(r"^spotlight_confirm/$", "dashboard.views.dash_confirm_index", name="confirm_dashboard"),

url(r"updates/$", "dashboard.views.receive_updates_api", name="receive_updates_api"),
url(r"^user_badges/$", "dashboard.views.user_badges", name="user_badges")
  #  url(r"^dashboard/spotlightrequest/$", "dashboard.views.dashboard_spotlight_request", name="spotlight_request"),
)
