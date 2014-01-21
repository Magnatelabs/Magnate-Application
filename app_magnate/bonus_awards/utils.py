from .models import BonusAward
from django.conf import settings

# username is a string, such as 'admin'
# Returns a Decimal
def total_bonus_amount(username):
    return sum([d.amount for d in BonusAward.objects.filter(user__username=username)])

