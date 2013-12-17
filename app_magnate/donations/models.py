from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from billing.signals import transaction_was_successful, transaction_was_unsuccessful
from django.dispatch import receiver
from dashboard.mixins import PrivatelyPublishedModelMixin
from decimal import Decimal
import datetime
import status_awards


class BillingInfo (models.Model):
#    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city =  models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    amount =  models.PositiveIntegerField(editable=False, default=0)

    def __unicode__(self):
        return self.first_name

class Donation (PrivatelyPublishedModelMixin, models.Model):
    user = models.ForeignKey(User)
    transaction_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '$%.2f by %s on %s' % (self.amount, self.user, self.timestamp)

    # Every donation will be automatically posted as a private message to the user, thanks to PrivatelyPublishedModelMixin. Some customization...

    #override
    def create_entry_title(self):
        return 'Thank you for your new donation!'

    #override
    def create_entry_content(self):
        return 'Fantastic! You have just donated $%.2f' % (self.amount)

    #override 
    def create_entry_slug(self):
        return 'donation'



    @receiver(transaction_was_successful)
    def on_transaction_was_successful(sender, **kwargs):
        if ('request' in kwargs) and (kwargs['request'].method=='POST'):
            data = kwargs['request'].POST

            try:
                user=User.objects.get(username=data['x_cust_id'])
            except User.DoesNotExist, e:
                # LOG FATAL ERROR
                print 'FATAL ERROR while saving a donation: User %s does not exist' % data['x_cust_id']
                return

            user = User.objects.get(username=data['x_cust_id'])
            amount = Decimal(data['x_amount'])
            transaction_id = data['x_trans_id']
            donation = Donation(user=user, amount=amount, transaction_id=transaction_id)  
            donation.save()
            status_awards.award_badges("user_donation", user)
            #import pdb; pdb.set_trace()
        


class FailedDonation (models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return '$%.2f by %s on %s' % (self.amount, self.user, self.timestamp)

    @receiver(transaction_was_unsuccessful)
    def on_transaction_was_unsuccessful(sender, **kwargs):
        pass
        #import pdb; pdb.set_trace()
