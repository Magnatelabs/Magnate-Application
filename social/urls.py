from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from social import views 
from social.views import feedback_entry 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
url(r"^social/like/$", "social.views.ajax_like_entry", name='ajax_like_entry'), 
url(r"^social/rate/$", "social.views.ajax_star_rating", name='ajax_star_rating'),
url(r"^users/$", "social.views.user_pages", name='user_page'),
url(r"^feedback/$", feedback_entry.as_view(), name="platform_main"),
)