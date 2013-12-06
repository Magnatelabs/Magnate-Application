from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from billing.signals import transaction_was_successful, transaction_was_unsuccessful
from django.dispatch import receiver

import datetime

class BillingInfo (models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city =  models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __unicode__(self):
        return self.first_name

class Donation (models.Model):
    user = models.ForeignKey(User)
    transaction_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '$%.2f by %s on %s' % (self.amount, self.user, self.timestamp)

    @receiver(transaction_was_successful)
    def on_transaction_was_successful(sender, **kwargs):
        print 'transaction successful'
        data = kwargs['request'].POST

        try:
            user=User.objects.get(username=data['x_cust_id'])
        except User.DoesNotExist, e:
            # LOG FATAL ERROR
            print 'FATAL ERROR while saving a donation: User %s does not exist' % data['x_cust_id']
            return

        user = User.objects.get(username=data['x_cust_id'])
        amount = data['x_amount']
        transaction_id = data['x_trans_id']
        donation = Donation(user=user, amount=amount, transaction_id=transaction_id)  
        donation.save()
        #import pdb; pdb.set_trace()


class FailedDonation (models.Model):
    user = models.ForeignKey(User)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    timestamp = models.DateTimeField()

    def __unicode__(self):
        return '$%.2f by %s on %s' % (self.amount, self.user, self.timestamp)

    @receiver(transaction_was_unsuccessful)
    def on_transaction_was_unsuccessful(sender, **kwargs):
        print 'transaction failed'
        #import pdb; pdb.set_trace()
