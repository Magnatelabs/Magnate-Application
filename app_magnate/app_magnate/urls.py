from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^waitinglist/", include("waitinglist.urls")),
#    url(r"^contacts/", include("phonebook.urls")),
#    url(r"^testform/", include("testFormApp.urls")),
    url(r"^startedsurvey/", include("getstartedquestions.urls")), 
    url(r"^aboutus/", include("companyinfo.urls")),
    url(r"^errors/", include("siteErrors.urls")),
    url(r"^dash/", include("dashboard.urls")),
    url(r"^donations/", include("donations.urls")),
    url(r"^status/", include("status_awards.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
