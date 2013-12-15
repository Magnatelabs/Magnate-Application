from .models import Donation
from django.conf import settings

# username is a string, such as 'admin'
# Returns a Decimal
def total_donation_amount(username):
    return sum([d.amount for d in Donation.objects.filter(user__username=username)])

def all_donations_by_user(username):
    return Donation.objects.filter(user__username=username)

