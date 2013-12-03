"""Urls for the Zinnia entries"""
from django.conf.urls import url
from django.conf.urls import patterns

from glue_zinnia.views import HiddenEntryDetail


urlpatterns = patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        HiddenEntryDetail.as_view(),
        name='zinnia_entry_detail'),
)
