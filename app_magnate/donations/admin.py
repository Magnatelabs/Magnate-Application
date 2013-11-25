from django.contrib import admin
from donations.models import Donation, FailedDonation

admin.site.register(Donation)
admin.site.register(FailedDonation)
