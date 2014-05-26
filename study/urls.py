from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import study_index 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^initial_submit/$", study_index.as_view(), name="study_index"),
  url(r"^initial_submit/confirmation$", "study.views.submit_completed", name="submit_completed"),
)
