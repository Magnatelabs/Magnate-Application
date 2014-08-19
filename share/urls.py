from django.conf.urls import patterns, url
from share.views import share_index 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
  url(r"^share_index/$", share_index.as_view(), name="sharelightbox"),
)