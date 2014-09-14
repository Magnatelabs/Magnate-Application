from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from groups import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^all/$", "groups.views.groups_index", name="groups_all"),
  url(r"^(?P<id>\d+)/$", "groups.views.groups_detail_home", name="category_home_page"),
  url(r"^info/$", "groups.views.groups_detail_information", name="groups_detail_info"),
  url(r"^current_objective/$", "groups.views.groups_detail_objective", name="groups_detail_objective"),

  url(r'^follow_category/(?P<id>\d+)/$', "groups.views.ajax_follow_category", name='follow_category'),
  
)
