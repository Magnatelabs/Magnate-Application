from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from zinnia.views.archives import EntryIndex


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/", include("account.urls")),
    url(r"^waitinglist/", include("waitinglist.urls")),

# We don't want to include all Zinnia.urls, as we do not want to expose
# everything to the users. It may be possible to e.g. decorate the include
# with login_required, see http://stackoverflow.com/questions/2307926/is-it-possible-to-decorate-include-in-django-urls-with-login-required
# I guess, it may even be possible to make zinnia.urls available
# only for certain users. For now we want them closed.
    url(r'^blog/', include('glue_zinnia.urls')),
#    url(r'^blg/', EntryIndex.as_view()),

# NOT SURE about this one... Needed for Zinnia...    
    url(r'^comments/', include('django.contrib.comments.urls')),

# However, then admin cannot work with Zinnia entries. It complains
# about NoReverseMatch, because it is trying to display a list of URLs
# linking to the posts on the website... So here we are faking it
# by allowing it to actually generate links, though those links
# won't lead to anywhere. (Double-check when upgrading Zinia 
# that it doesn't create any security holes, though it shouldn't).
#
# TODO: perhaps just remove the URL column from the Zinnia Entry in
# admin... 
# TODO: ideally, include zinnia.urls, but decorate them somehow so that
# only root (or certain users) would be able to view them. This would
# be nice for the admin - to see all posts, etc.
#    url(r'^zinnia_shortlink/', include('zinnia.urls.shortlink')),

#    url(r"^contacts/", include("phonebook.urls")),
#    url(r"^testform/", include("testFormApp.urls")),
    url(r"^startedsurvey/", include("getstartedquestions.urls")), 
    url(r"^aboutus/", include("companyinfo.urls")),
    url(r"^errors/", include("siteErrors.urls")),
    url(r"^dash/", include("dashboard.urls")),
    url(r"^social/", include("social.urls")),
    url(r"^donations/", include("donations.urls")),
    url(r"^status/", include("status_awards.urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
