from django.test import TestCase

class DonationTestCase(TestCase):
    def test_successfull_donation(self):
        """Authorize.net donation went through"""
        print "hello went through"

    def test_failed_donation(self):
        """Authorize.net donation did not go through"""
        print "sucks bro"

