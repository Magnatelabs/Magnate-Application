from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from dashboard import views 

#for the FormView
from dashboard.views import DashboardView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^dashboard/$", DashboardView.as_view(), name="dashboard"),
  url(r"updates/$", "dashboard.views.receive_updates_api", name="receive_updates_api"),
  url(r"^user_badges/$", "dashboard.views.user_badges", name="user_badges")
)
