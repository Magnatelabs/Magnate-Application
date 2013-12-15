import donations.utils as du
from brabeion.models import BadgeAward


def magnate_status_badge(user):
    if not user.is_authenticated():
        return None
    # Returning the latest awarded status badge
    # Theoretically might get it wrong if two were awarded at the same moment
    # But shouldn't be a problem if we don't go crazy creating multiple levels of badges awarded for other badges awarded for other badges
    for badge in user.badges_earned.order_by('-awarded_at'):
        if badge.is_metabadge():
            return badge
    return None


def magnate_user_info(request):
    feed=du.all_donations_by_user(request.user)
    total_donation_amount = du.total_donation_amount(request.user)
    user_has_donation = (total_donation_amount > 0)
    status_badge = magnate_status_badge(request.user)
    has_status_badge = (status_badge is not None)

    return {'feed': feed, 'total_donation_amount': total_donation_amount, 'user_has_donation': user_has_donation, 'has_status_badge': has_status_badge, 'status_badge': status_badge}
