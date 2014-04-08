from models import get_stat

def website_stats(request):
    website_total_donation_amount = get_stat("TOTAL_DONATION_AMOUNT")

    return {'website_total_donation_amount' : website_total_donation_amount}
