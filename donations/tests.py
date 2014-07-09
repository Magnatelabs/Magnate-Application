from django.test import TestCase
from django.test import Client
from billing.signals import transaction_was_successful, transaction_was_unsuccessful
import billing
from django.dispatch import receiver

from decimal import Decimal
from .models import Donation
from django.contrib.auth import get_user_model
from django.conf import settings
import hashlib

from zinnia.models.entry import Entry
from dashboard.mixins import PrivatelyPublishedModelMixin
from zinnia.managers import HIDDEN
import status_awards

class DonationZinniaTestCase(TestCase):
    def setUp(self):
        self.user=get_user_model()(username='green_elephant!!!')
        self.user.save()

    def is_private_entry(self, entry, user):
        self.assertEqual(entry.status, HIDDEN, "The entry should be private, i.e. status==HIDDEN")
        self.assertTrue(self.user in entry.authorized_users.all(), "The user should be authorized to view this entry")
        self.assertEquals(len(entry.authorized_users.all()), 1, "Only this user should be authorized to view this entry; nobody else") 
        return True

    def test_donation_entry(self):
        # Every time a new Donation is saved, a new private message should be sent to the user
        self.assertTrue(issubclass(Donation, PrivatelyPublishedModelMixin))

        d=Donation(amount=3.14, user=self.user)
        d.save()
        
        l=Entry.objects.all()
        self.assertEquals(len(l), 1)
        self.assertEquals(l[0], d.entry)
        entry = d.entry
        
        self.assertTrue(self.is_private_entry(entry, self.user))
        self.assertTrue('3.14' in entry.content, '3.14 is the domation amount. It should be mentioned somewhere in the message, shouldn''t it?')

    def test_donation_badge(self):
        d=Donation(amount=123.4567, user=self.user)
        d.save()
        # For now we have to explicitly call award_badges ---
        # and it is called in certain places in the code.
        # In the future, if the badges will be given via an overload of save()
        # on some models and/or after receiving a signal, then the tests should be adjusted.
        self.assertEquals(self.user.badges_earned.count(), 0)
        status_awards.award_badges("user_donation", self.user)
        self.assertEquals(self.user.badges_earned.count(), 1)
        badge_award = self.user.badges_earned.all()[0]
        self.assertEquals(badge_award.slug, 'donated-something')

        l = Entry.objects.all()
        self.assertEquals(len(l), 2, "There should be two entries: about the donation and about the badge")
        self.assertTrue( ((l[0]==badge_award.entry) and (l[1]==d.entry)) or ((l[1]==badge_award.entry) and (l[0]==d.entry)) )
        for e in l:
            self.assertTrue(self.is_private_entry(e, self.user))
        self.assertTrue('This badge is given for any donation' in badge_award.entry.content)
        self.assertTrue('123.46' in d.entry.content, "The donation amount was #123.4567, so 123.46 (due to rounding) should be mentioned somewhere in the entry")


class DonationTestCase(TestCase):
    
    # The user fills a form with credit card info, etc. and clicks "Pay".
    # The info goes to Authorize.net. The form contains a hidden field
    # with the URL where Authorize.net sends a response. The response will be
    # a POST http request with the following fields. And we are now testing
    # how our app processes and responds to this response. Our app should
    # respond with a code snippet that Authorize.net will then serve to
    # redirect the user's browser. Our app should also record the transaction
    # if it was successful.

    
    def set_constants(self):
        self.TEST_EMAIL = u'ewifjoi23@gmail.com'
        self.TEST_AMOUNT=Decimal(23.1268327) # purposely many digits after the decimal!
        self.TEST_TRANS_ID=u'2202244589'
        self.TEST_MD5_HASH=self.compute_authorize_net_md5_hash(self.TEST_TRANS_ID, self.TEST_AMOUNT)
        self.authorize_net_success_request_POST = {u'x_response_reason_text': [u'This transaction has been approved.'], u'x_fax': [u''], u'x_auth_code': [u'XYWDLN'], u'x_ship_to_zip': [u''], u'x_phone': [u''], u'x_ship_to_last_name': [u''], u'x_cavv_response': [u'2'], u'x_ship_to_state': [u''], u'x_cust_id': [self.TEST_EMAIL], u'x_zip': [u'95455'], u'x_amount': [unicode(self.TEST_AMOUNT)], u'x_ship_to_company': [u''], u'x_freight': [u'0.00'], u'x_method': [u'CC'], u'x_email': [u''], u'x_test_request': [u'false'], u'x_card_type': [u'Visa'], u'x_ship_to_first_name': [u''], u'x_last_name': [u'Cardpoop'], u'x_trans_id': [self.TEST_TRANS_ID], u'x_company': [u''], u'x_tax': [u'0.00'], u'x_tax_exempt': [u'FALSE'], u'x_avs_code': [u'Y'], u'x_ship_to_city': [u''], u'x_address': [u'132 afsaaksn'], u'x_po_num': [u''], u'x_account_number': [u'XXXX8888'], u'x_type': [u'auth_capture'], u'x_description': [u''], u'x_ship_to_address': [u''], u'x_MD5_Hash': [u'78178FB8746F96A3618E19E357F43242'], u'x_ship_to_country': [u''], u'x_cvv2_resp_code': [u'P'], u'x_city': [u'What'], u'x_response_code': [u'1'], u'x_country': [u'USA'], u'x_invoice_num': [u''], u'x_first_name': [u'JCB'], u'x_response_reason_code': [u'1'], u'x_duty': [u'0.00'], u'x_state': [u'CA']}

    
    def reset_counts(self):
        DonationTestCase.success_count=0
        DonationTestCase.unsuccess_count=0

    def setUp(self):
        merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
        if not merchant_settings or not merchant_settings.get("authorize_net"):
            raise("The '%s' integration is not correctly configured." % self.display_name)
        self.authorize_net_settings = merchant_settings["authorize_net"]
        self.set_constants()
        
        self.client = Client()
        self.reset_counts()
        get_user_model()(username=self.TEST_EMAIL).save()


    # Computes the correct MD5_HASH to sign an Authorize.NET response
    # To make it look authentic
    # x_trans_id is a string, such as '2202244589'
    # x_amount is a string, such as '1.00'
    def compute_authorize_net_md5_hash(self, x_trans_id, x_amount):
        md5_hash = self.authorize_net_settings["MD5_HASH"]
        login_id = self.authorize_net_settings["LOGIN_ID"]
        hash_str = "%s%s%s%s" % (md5_hash, login_id, x_trans_id, x_amount)
        return hashlib.md5(hash_str).hexdigest()



    @receiver(transaction_was_successful)
    def on_transaction_was_successful(sender, **kwargs):
        assert isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration) or isinstance(sender, billing.gateways.authorize_net_gateway.AuthorizeNetGateway)
        if isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration):
            assert 'request' in kwargs
            assert kwargs['request'].META['REQUEST_METHOD']=='POST'
        

            DonationTestCase.success_count += 1
        

    @receiver(transaction_was_unsuccessful)
    def on_transaction_was_unsuccessful(sender, **kwargs):
        assert isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration) or isinstance(sender, billing.gateways.authorize_net_gateway.AuthorizeNetGateway)
        if  isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration):

            assert 'request' in kwargs
            assert kwargs['request'].META['REQUEST_METHOD']=='POST'

            DonationTestCase.unsuccess_count += 1
        

    def test_successful_donation(self):
        """Authorize.net donation went through"""
        print "hello went through"
        self.reset_counts()


        c = self.client
        response_forbidden = c.post('/fund/authorize_net/authorize_net-notify-handler/', self.authorize_net_success_request_POST)
        # The MD5 Hash that we had by default is wrong. So expect 403 error, because the app can't
        # verify that the request came from Authorize.net.
        self.assertEqual(response_forbidden.status_code, 403)
        # Fixing the md5 hash
        self.authorize_net_success_request_POST['x_MD5_Hash'] = self.TEST_MD5_HASH
        # Now it's signed with the proper MD5 hash. Should succeed.
        response = c.post('/fund/authorize_net/authorize_net-notify-handler/', self.authorize_net_success_request_POST)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(DonationTestCase.success_count, 1)
        self.assertEqual(DonationTestCase.unsuccess_count, 0)

        self.assertEqual(len(Donation.objects.all()), 1)
        donation = Donation.objects.latest('timestamp')
        self.assertIsNotNone(donation, "The payment was processed successfully. A Donation model object should have been saved to the database")

        self.assertAlmostEqual(donation.amount, self.TEST_AMOUNT, places=2)
        self.assertEqual(donation.transaction_id, self.TEST_TRANS_ID)
        self.assertEqual(unicode(donation.user), self.TEST_EMAIL)
       # import pdb; pdb.set_trace()


    def test_failed_donation(self):
        """Authorize.net donation did not go through"""


