from django.test import TestCase
from django.test import Client
from billing.signals import transaction_was_successful, transaction_was_unsuccessful
import billing
from django.dispatch import receiver

from .models import Donation
from django.contrib.auth import get_user_model

class DonationTestCase(TestCase):
    
    # The user fills a form with credit card info, etc. and clicks "Pay".
    # The info goes to Authorize.net. The form contains a hidden field
    # with the URL where Authorize.net sends a response. The response will be
    # a POST http request with the following fields. And we are now testing
    # how our app processes and responds to this response. Our app should
    # respond with a code snippet that Authorize.net will then serve to
    # redirect the user's browser. Our app should also record the transaction
    # if it was successful.

    
    TEST_EMAIL = u'ewifjoi23@gmail.com'
    authorize_net_success_request_POST = {u'x_response_reason_text': [u'This transaction has been approved.'], u'x_fax': [u''], u'x_auth_code': [u'XYWDLN'], u'x_ship_to_zip': [u''], u'x_phone': [u''], u'x_ship_to_last_name': [u''], u'x_cavv_response': [u'2'], u'x_ship_to_state': [u''], u'x_cust_id': [TEST_EMAIL], u'x_zip': [u'95455'], u'x_amount': [u'1.00'], u'x_ship_to_company': [u''], u'x_freight': [u'0.00'], u'x_method': [u'CC'], u'x_email': [u''], u'x_test_request': [u'false'], u'x_card_type': [u'Visa'], u'x_ship_to_first_name': [u''], u'x_last_name': [u'Cardpoop'], u'x_trans_id': [u'2202244589'], u'x_company': [u''], u'x_tax': [u'0.00'], u'x_tax_exempt': [u'FALSE'], u'x_avs_code': [u'Y'], u'x_ship_to_city': [u''], u'x_address': [u'132 afsaaksn'], u'x_po_num': [u''], u'x_account_number': [u'XXXX8888'], u'x_type': [u'auth_capture'], u'x_description': [u''], u'x_ship_to_address': [u''], u'x_MD5_Hash': [u'78178FB8746F96A3618E19E357F43242'], u'x_ship_to_country': [u''], u'x_cvv2_resp_code': [u'P'], u'x_city': [u'What'], u'x_response_code': [u'1'], u'x_country': [u'USA'], u'x_invoice_num': [u''], u'x_first_name': [u'JCB'], u'x_response_reason_code': [u'1'], u'x_duty': [u'0.00'], u'x_state': [u'CA']}

    
    def reset_counts(self):
        DonationTestCase.success_count=0
        DonationTestCase.unsuccess_count=0

    def setUp(self):
        self.client = Client()
        self.reset_counts()
        get_user_model()(username=self.TEST_EMAIL).save()

    @receiver(transaction_was_successful)
    def on_transaction_was_successful(sender, **kwargs):
        assert isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration)
        assert 'request' in kwargs
        assert kwargs['request'].META['REQUEST_METHOD']=='POST'
        

        DonationTestCase.success_count += 1
        print 'success'

    @receiver(transaction_was_unsuccessful)
    def on_transaction_was_onsuccessful(sender, **kwargs):
        assert isinstance(sender, billing.integrations.authorize_net_dpm_integration.AuthorizeNetDpmIntegration)
        assert 'request' in kwargs
        assert kwargs['request'].META['REQUEST_METHOD']=='POST'

        DonationTestCase.unsuccess_count += 1
        print 'failed'

    def test_successful_donation(self):
        """Authorize.net donation went through"""
        print "hello went through"
        self.reset_counts()


        c = self.client
        response = c.post('/donations/authorize_net/authorize_net-notify-handler/', self.authorize_net_success_request_POST)
#        print response 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DonationTestCase.success_count, 1)
        self.assertEqual(DonationTestCase.unsuccess_count, 0)

        self.assertIsNotNone(Donation.objects.last(), "The payment was processed successfully. A Donation model object should have been saved to the database")


    def test_failed_donation(self):
        """Authorize.net donation did not go through"""
        print "sucks bro"
