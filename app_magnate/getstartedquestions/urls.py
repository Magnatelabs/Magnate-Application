from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from getstartedquestions import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^started_survey/$", "getstartedquestions.views.survey_index", name="startedsurvey"),
                       )
