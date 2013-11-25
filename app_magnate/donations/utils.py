from .models import Donation

# username is a string, such as 'admin'
# Returns a Decimal
def total_donation_amount(username):
    return sum([d.amount for d in Donation.objects.filter(user__username=username)])
