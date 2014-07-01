from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from status_awards import views 

#for the FormView
#from dashboard.views import dashboard_spotlight_request 

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns("",
  url(r"^home/$", "status_awards.views.status_index", name="status_home"),
  url(r"^award_detail/$", "status_awards.views.award_detail", name="status_award_detail"),
  url(r"^newhome/$", "status_awards.views.newstatus_index", name="newstatus_home"),
)
