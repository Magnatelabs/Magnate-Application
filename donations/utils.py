from .models import Donation
from django.conf import settings
import datetime

# username is a string, such as 'admin'
# Returns a Decimal
def total_donation_amount(username):
    return sum([d.amount for d in Donation.objects.filter(user__username=username)])

def all_donations_by_user(username):
    return Donation.objects.filter(user__username=username)

def donation_vesting_date(username):
    return datetime.datetime(2015,1,1)
