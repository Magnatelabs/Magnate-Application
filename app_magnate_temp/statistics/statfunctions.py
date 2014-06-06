from django.db.models import Sum

from models import set_stat

def update_statistics():
    from donations.models import Donation
#    set_stat("TOTAL_DONATION_AMOUNT', sum([d.amount for d in donation.objects.all()])

    set_stat("TOTAL_DONATION_AMOUNT", Donation.objects.aggregate(Sum('amount'))['amount__sum'] )
    
