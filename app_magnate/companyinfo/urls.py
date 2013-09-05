from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from companyinfo import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^about_us/$", "companyinfo.views.aboutus_index", name="aboutus"),
  url(r"^newslettersignup/$", "companyinfo.views.newsletter_signup", name="mediaupdates"),
)
