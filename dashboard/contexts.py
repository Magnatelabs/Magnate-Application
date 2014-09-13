import donations.utils as du
from brabeion.models import BadgeAward
from forum.views.admin import get_recent_activity



# Choosing which badge to display as the status badge.
# Choosing the latest metabadge. Since the precision is only up to a second,
# this may not work in case of multiple badges awarded at the same time.
# In this case picking the latest sql id among those with the latest
# awarded_at. 
def magnate_status_badge(user):
    if not user.is_authenticated():
        return None

    for badge in user.badges_earned.order_by('-awarded_at', '-id'):
        if badge.is_metabadge():
            return badge
    return None


def magnate_user_info(request):
    # just a Django queryset
    recent_activity = get_recent_activity().exclude(user=request.user)

    feed=du.all_donations_by_user(request.user)
    total_donation_amount = du.total_donation_amount(request.user)
    user_has_donation = (total_donation_amount > 0)
    status_badge = magnate_status_badge(request.user)
    dvd = du.donation_vesting_date(request.user)
    has_status_badge = (status_badge is not None)

    return {'recent_activity': recent_activity, 'feed': feed, 'total_donation_amount': total_donation_amount, 'user_has_donation': user_has_donation, 'has_status_badge': has_status_badge, 'status_badge': status_badge, 'donation_vesting_date': dvd}


