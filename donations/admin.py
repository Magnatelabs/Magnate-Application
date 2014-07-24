from django.contrib import admin
from donations.models import Donation, MagnateFund, PortfolioCompany

admin.site.register(Donation)
admin.site.register(MagnateFund)
admin.site.register(PortfolioCompany)

