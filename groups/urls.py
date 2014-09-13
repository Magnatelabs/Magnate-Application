from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from groups import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^all/$", "groups.views.groups_index", name="groups_all"),
  url(r"^home/$", "groups.views.groups_detail_home", name="groups_detail_home"),
  url(r"^info/$", "groups.views.groups_detail_information", name="groups_detail_info"),
  url(r"^current_objective/$", "groups.views.groups_detail_objective", name="groups_detail_objective"),
)