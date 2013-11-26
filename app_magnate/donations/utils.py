from .models import Donation
from django.conf import settings

# username is a string, such as 'admin'
# Returns a Decimal
def total_donation_amount(username):
    return sum([d.amount for d in Donation.objects.filter(user__username=username)])

def all_donations_by_user(username):
    return Donation.objects.filter(user__username=username)

def all_badges_for_user(username):
    l=  [{'as_html': "<img src=\"%s\" alt=\"%s\" />" % (settings.STATIC_URL + 'img/img_icon13.png', 'BADGE')}, {'as_html': "<img src=\"%s\" alt=\"%s\" />" % (settings.STATIC_URL + 'img/img_icon14.png', 'BADGE')}, {'as_html': "<img src=\"%s\" alt=\"%s\" />" % (settings.STATIC_URL + 'img/img_icon15.png', 'BADGE')}]
    if all_donations_by_user(username)>1.0:
        return l+l+l
    else:
        return []
