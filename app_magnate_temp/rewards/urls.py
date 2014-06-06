from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from companyinfo import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^$", "rewards.views.rewards_index", name="rewards"),
)
