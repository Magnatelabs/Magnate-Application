import donations.utils as du
from brabeion.models import BadgeAward
from forum.views.admin import get_recent_activity

import logging
logger=logging.getLogger(__name__)


# Choosing which badge to display as the status badge.
# Choosing the latest metabadge. Since the precision is only up to a second,
# this may not work in case of multiple badges awarded at the same time.
# In this case picking the latest sql id among those with the latest
# awarded_at. 
def magnate_status_badge(user):
    try:
        if not user.is_authenticated():
            return None

        for badge in user.badges_earned.order_by('-awarded_at', '-id'):
            if badge.is_metabadge():
                return badge
        return None
    except:
        logging.exception("Error while retrieving magnate status badge for user '%s'" % str(user))
        return None

# Stupid patch to disable recent activity while testing.
# Somehow django generates ... WHERE NOT... in a query when we are
# using exclude, and this does not work with SQLite. I don't know who is guilty
# here. Should perhaps submit a ticket to Django...
# Just print get_recent_activity().exclude(user=request.user); you will see...
from django.conf import settings
if not settings.TESTING:
    recent_activity_f = lambda user: get_recent_activity().exclude(user=user)
else:
    recent_activity_f = lambda user: []

def magnate_user_info(request):
    # just a Django queryset
    recent_activity = recent_activity_f(request.user)

    feed=du.all_donations_by_user(request.user)
    total_donation_amount = du.total_donation_amount(request.user)
    user_has_donation = (total_donation_amount > 0)
    status_badge = magnate_status_badge(request.user)
    dvd = du.donation_vesting_date(request.user)
    has_status_badge = (status_badge is not None)

    return {'recent_activity': recent_activity, 'feed': feed, 'total_donation_amount': total_donation_amount, 'user_has_donation': user_has_donation, 'has_status_badge': has_status_badge, 'status_badge': status_badge, 'donation_vesting_date': dvd}


