from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from groups import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^home/$", "groups.views.groups_index", name="groups_home"),
)
