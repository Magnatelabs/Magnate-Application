from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from social import views 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
url(r"^social/like/$", "social.views.ajax_like_entry", name='ajax_like_entry'),                       
)