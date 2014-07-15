from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from glue_osqa import views 

#for the FormView
#from dashboard.views import dashboard_spotlight_request 

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns("",
  url(r"^question/$", "glue_osqa.views.question_page", name="question_page"),
)