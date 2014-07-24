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
import logging

from statistics.statfunctions import update_statistics
from django.utils.translation import ugettext_lazy as _

from caching.base import CachingManager, CachingMixin
# See https://cache-machine.readthedocs.org/en/latest/ about caching

UPLOAD_COMPANY_LOGO_TO = 'uploads/funds'

class MagnateFund (CachingMixin, models.Model):
    name = models.CharField(
        _('name'), max_length=200)

    description = models.TextField(
        _('description'), default="")

    is_active = models.BooleanField(
        _('is active'), default=True)

    objects = CachingManager()

    def __unicode__(self):
        return 'Fund: %s' % (self.name)

    def is_visible(self, user):
        """
        Checks if the user can see the fund on his fund page.
        In the future can depend on the status of the user.
        """
        return self.is_active


class PortfolioCompany (models.Model):
    
    fund = models.ForeignKey('MagnateFund')

    name = models.CharField(
        _('company name'), max_length=200)

    description = models.TextField(
        _('company description'), default="")

    tags = models.CharField(
        _('tags'), max_length=400, default="")

    image = models.ImageField(
        _('company logo'), blank=True, upload_to=UPLOAD_COMPANY_LOGO_TO)

    def __unicode__(self):
        return 'Investment. Company: %s, Fund: %s' % (self.name, self.fund.name)


#FUND_CHOICES = ((DRAFT, _('draft')),
#                (HIDDEN, _('Magnate Permanent Fund (MPF)')),
#                (PUBLISHED, _('Magnate Multi-Strategy Fund (MMSF)')))#
#
#class PortfolioCompany (models.Model):#
#
#    name = models.CharField(max_length=200)

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


    @receiver(transaction_was_unsuccessful)
    def on_transaction_was_unsuccessful(sender, **kwargs):
        if ('request' in kwargs) and (kwargs['request'].method=='POST'):
            data = kwargs['request'].POST

            try:
                user=User.objects.get(username=data['x_cust_id'])
            except User.DoesNotExist, e:
                logging.error('Error while processing a failed donation: User %s does not exist' % data['x_cust_id'])
                return
            user=User.objects.get(username=data['x_cust_id'])
            x_response_code=data['x_response_code']
            x_response_reason_code=data['x_response_reason_code']            

            logging.warn('FAILED DONATION. User: %s, code: %s, reason: %s' % (user, x_response_code, x_response_reason_code))

    @receiver(transaction_was_successful)
    def on_transaction_was_successful(sender, **kwargs):
        if ('request' in kwargs) and (kwargs['request'].method=='POST'):
            data = kwargs['request'].POST

            try:
                user=User.objects.get(username=data['x_cust_id'])
            except User.DoesNotExist, e:
                logging.fatal('Error while processing a successful donation: User %s does not exist' % data['x_cust_id'])
                return

            user = User.objects.get(username=data['x_cust_id'])
            amount = Decimal(data['x_amount'])
            transaction_id = data['x_trans_id']
            donation = Donation(user=user, amount=amount, transaction_id=transaction_id)  
            donation.save()

            logging.info('OK, DONATION SUCCESSFUL. User: %s, transaction_id: %s' % (user, transaction_id))
            status_awards.award_badges("user_donation", user)
            update_statistics() # This function is called to upadte the TOTAL_DONATION_AMOUNT
            #import pdb; pdb.set_trace()
        

