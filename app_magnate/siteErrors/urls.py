from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from siteErrors import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^404/$", "siteErrors.views.index_404", name="error404"),
  url(r"^500/$", "siteErrors.views.index_500", name="error500"),
)
