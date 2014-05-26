"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.db import settings
from urlparse import urlparse
from urllib import urlencode

class SimpleTest(TestCase):
    def test_dashboard(self):
        client = Client()
        response = client.get(reverse('dashboard'))

        # Expecting redirect because of login_required
        self.assertEqual(response.status_code, 302)

        # Let's make sure we are redirected to the right place
        url_next=response._headers['location'][1] # 'http://testserver/accounts/login/?next=/dash/dashboard/'
        parsed=urlparse(url_next);

#        try:
#            login_url=settings.LOGIN_URL
#        except:
        login_url=reverse('account_login')

        self.assertEqual(parsed.scheme, 'http');
        self.assertEqual(parsed.netloc, 'testserver');
        self.assertEqual(parsed.path, login_url);
        self.assertEqual(parsed.params, '');
        self.assertEqual(parsed.query, 'next='+reverse('dashboard'))# urlencode({'next': reverse('dashboard')}));
        self.assertEqual(parsed.fragment, '');
        
        # Now try to follow the redirect
        response = client.get(reverse('dashboard'), follow=True)
        self.assertEqual(response.status_code, 200, "response.status_code=%d, not 200; response.redirect_chain==%s" % (response.status_code, response.redirect_chain))

