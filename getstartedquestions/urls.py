from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from getstartedquestions import views 
from getstartedquestions.views import survey_index 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^started_survey/$", survey_index.as_view(), name="startedsurvey"),
  url(r"^started_confirm/$", "getstartedquestions.views.confirmation_index", name="confirm_questions"),
)
