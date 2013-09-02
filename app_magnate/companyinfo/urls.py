from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from startedQuestionnaire import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^about_us/$", "companyinfo.views.aboutus_index", name="aboutus"),
)
