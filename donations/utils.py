from .models import Donation
from django.conf import settings
import datetime
from django.db.models import Sum

# username is a string, such as 'admin'
# Returns a Decimal
def total_donation_amount(username):
    result = sum([d.amount for d in Donation.objects.filter(user__username=username)])
#    assert result == Donation.objects.filter(user__username=username).aggregate(total_donation_amount=Sum('amount')) ['total_donation_amount']
    return result 

def all_donations_by_user(username):
    return Donation.objects.filter(user__username=username)

def no_objective_total(username):
    result = sum([d.amount for d in Donation.objects.filter(user__username=username, objective__isnull=True)])
  #  assert result == Donation.objects.filter(user__username=username, objective__isnull=True).aggregate(amount_no_objective=Sum('amount'))['amount_no_objective']
    return result
