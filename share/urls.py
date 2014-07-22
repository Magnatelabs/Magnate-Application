from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from share import views 
from share.views import share_index 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^share_index/$", share_index.as_view(), name="sharelightbox"),
  url(r"^started_confirm/$", "getstartedquestions.views.confirmation_index", name="confirm_questions"),
)