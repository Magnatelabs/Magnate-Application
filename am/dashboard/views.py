from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.http import require_http_methods
import datetime
from django.utils import simplejson
from django.http import HttpResponse

#imports to recognize django messages
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


#import to recognize class based view
from django.views.generic.edit import FormView

from donations.utils import total_donation_amount, all_donations_by_user

import zinnia
from zinnia.views.archives import EntryIndex

# for /updates/
from zinnia.models.entry import Entry
import time
from django.template import loader, Context

def dashboard_index(request):
    if not request.user.is_authenticated():
        return redirect('/account/login/?next=%s' % request.path)

    feed=all_donations_by_user(request.user)
    tda = total_donation_amount(request.user)
    user_has_donation = (tda > 0)

    user_badges = all_badges_for_user(request.user)
 

    return EntryIndex.as_view()(request, 'dashboard/dashboard_main.html', {'user_has_donation': True} )

#    return render(request, 'dashboard/dashboard_main.html', {'user_has_donation': user_has_donation, 'feed': feed, 'total_donation_amount': tda, 'user_badges': user_badges})




from zinnia.models.entry import Entry

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class DashboardView(zinnia.views.archives.EntryIndex):

    # Login is required to view the dashboard.
    # Perhaps we can switch to using login_required middleware later. Then we won't need this.
    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, *args, **kwargs):
        return super(DashboardView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        assert self.request.user.is_authenticated(), "No user is logged in. Why are we trying to render a page? The user should have been redirected to a login page. In fact, all views in %s should be decorated with @login_required." % (self.__class__.__name__)

        # Completely override parent's get_queryset instead of merging 
        # parent's queryset with some other entries.
        #
        # TODO: make sure that we are getting Entries in a sorted order!
        # QUESTION: how is it achieved in Zinnia?
        return Entry.private.authorized_or_published(self.request.user)


def dash_confirm_index(request):
    return render(request, 'dashboard/dashboard_confirm.html')

def user_badges(request):
    if 'user_id' in request.GET:
        user = get_object_or_404(get_user_model(), pk=request.GET['user_id'])
        from .contexts import magnate_status_badge
        user_status_badge = magnate_status_badge(user)
        user_has_status_badge = (user_status_badge is not None)
        vars = {'user': user, 'user_status_badge': user_status_badge, 'user_has_status_badge': user_has_status_badge} 
    else:
        user = request.user
        if not user.is_authenticated():
            return HttpResponse(status=404)
        vars = {'user': user}
    return render(request, 'dashboard/__user_badges.html', vars)

@login_required
@require_http_methods(["GET"])
def receive_updates_api(request):
    try:
        strictlyafter=int(request.GET["strictlyafter"])
    except ValueError:
        strictlyafter=0

    last_ts=strictlyafter
    vars={"last_ts": 0, "entries": [], "badges": []}
    from zinnia.models.entry import Entry
    l = vars["entries"]
    # TODO FIXME: query by time. Do not ask for all entries
    for e in Entry.private.authorized_or_published(request.user).all():
        ts=int(time.mktime(e.creation_date.timetuple())*1000)
        if ts > strictlyafter:
            l.append({"slug": e.slug, "ts": ts})
            last_ts = max(last_ts, ts)

    l=vars["badges"]
    for badge in request.user.badges_earned.all():
        # TODO FIXME are badges' tiemstamps timezone aware???
        ts=int(time.mktime(badge.awarded_at.timetuple())*1000)
        if ts > strictlyafter:
            l.append({"name": badge.name, "slug": badge.slug, "level": badge.level, "ts": ts})
            last_ts = max(last_ts, ts)

    vars["last_ts"]=last_ts


    return HttpResponse(simplejson.dumps(vars), mimetype='application/javascript')
