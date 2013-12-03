import donations.utils as du


def magnate_user_info(request):
    feed=du.all_donations_by_user(request.user)
    total_donation_amount = du.total_donation_amount(request.user)
    user_has_donation = (total_donation_amount > 0)
    user_badges = du.all_badges_for_user(request.user)
    return {'feed': feed, 'total_donation_amount': total_donation_amount, 'user_has_donation': user_has_donation, 'user_badges': user_badges}
