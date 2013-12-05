"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class SimpleTest(TestCase):
    def test_dashboard(self):
        client = Client()
        response = client.get(reverse('dashboard'))

        # Expecting redirect because of login_required
        self.assertEqual(response.status_code, 302)

        url_next=response._headers['location'][1] # 'http://testserver/accounts/login/?next=/dash/dashboard/'
    
        # TODO: there may be more robust way to express it
        self.assertEqual('http://testserver/accounts/login/?next=%s' % (reverse('dashboard')), url_next)
