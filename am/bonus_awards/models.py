from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from dashboard.mixins import PrivatelyPublishedModelMixin
from decimal import Decimal
import datetime
import status_awards


class BonusAward(PrivatelyPublishedModelMixin, models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    reason = models.CharField(max_length=255)

    def __unicode__(self):
        return '$%.2f for %s on %s' % (self.amount, self.user, self.timestamp)

    # Every  will be automatically posted as a private message to the user, thanks to PrivatelyPublishedModelMixin. Some customization...

    #override
    def create_entry_title(self):
        return 'You just received a cash bonus!'

    #override
    def create_entry_content(self):
        return 'Wowza! Enjoy that extra $%.2f.' % (self.amount)

    #override 
    def create_entry_slug(self):
        return 'bonus'
