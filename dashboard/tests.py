"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from urlparse import urlparse
from urllib import urlencode

from app_magnate.unittest import create_test_user
from bs4 import BeautifulSoup
from Queue import Queue

class SimpleTest(TestCase):
    # Need the fixture so the Funds page works properly.
    fixtures=['fixtures/funds.json',]

    def test_links(self):
        c = Client()
        user = create_test_user('temporary', 'temporary@gmail.com', 
'temporary')
        c.login(username='temporary', password='temporary')


        q=Queue()
        mark={reverse('dashboard') : False}
        q.put(reverse('dashboard'))

        external=set()
        while not q.empty():
            url = q.get()
#            print 'checking %s' % (url)
            mark[url] = True
            r = c.get(url, follow=True)
            self.assertEqual(r.status_code, 200)
            soup = BeautifulSoup(r.content)
            outgoing=set()
            for link in soup.find_all('a'):
                outgoing.add(link.get('href'))
#            for form in soup.find_all('form'):
#                outgoing.add(form.get('action'))
            for child in outgoing:
                if child is not None: # some links have no href
                    self.assertEquals(type(child), unicode)
                    if child[0]=='/': # internal
                        if not child in mark:
                            mark[child]=False
                            q.put(child)
                    elif child[:4]=='http': # external
                        external.add(child)
        # Those pages must be reachable from the dashboard:
        self.assertTrue(mark[reverse('fund_home')])
        self.assertTrue(mark[reverse('groups_all')])
        self.assertTrue(mark[reverse('newstatus_home')])
        self.assertTrue(mark[reverse('donations_add')])
        
#        for url in external:
#            print 'External url: %s' % (url)

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

