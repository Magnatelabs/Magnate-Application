"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from app_magnate.unittest import create_test_user
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
User=get_user_model()
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from django.conf import settings
from django.db import models, connection

from zinnia.models.entry import Entry
from zinnia.models.author import Author
from zinnia.models.category import Category
from zinnia.managers import DRAFT, HIDDEN, PUBLISHED
import datetime, pytz

class SimpleZinniaTest(TestCase):
    def test_settings(self):
        # Check whether 'zinnia' is in INSTALLED APPS
        self.assertTrue('zinnia' in settings.INSTALLED_APPS)
 
        # Make sure that we have all Zinnia tables properly created in sqlite3
        cursor = connection.cursor()
        cursor.execute("SELECT name from sqlite_master WHERE type='table'")

        tables= cursor.fetchall()
#        print tables
        for t in [ 'zinnia_category', 'zinnia_entry_sites', 'zinnia_entry_related', 'zinnia_entry_authors', 'zinnia_entry_categories', 'zinnia_entry_authorized_users', 'zinnia_entry']:
            self.assertTrue((t,) in tables, 'Table \'%s\' not found' % (t))
        

    def test_basic_zinnia(self):
        self.assertTrue(issubclass(Entry, models.Model))
        self.assertTrue(issubclass(Author, models.Model))
        self.assertTrue(issubclass(Category, models.Model))

        # Try saving to see if the tables were created.
        Entry().save()
        Author().save()
        Category().save()

    def test_restricted_access(self):
        client = Client()
 
        user_g = create_test_user("Guido van Rossum", "email@ppyytthhoonn.org", "3jh3j")
        user_h = create_test_user("Hilda von Varden", "adverse@bluehouse.gro", "777777777")

        # must specify slug. Otherwise get_aboslute_url is broken and will get NoReverseMatch.



        entry = Entry(title="Django's wonderful permalink decorator 12321", slug="django", status=PUBLISHED, start_publication=datetime.datetime(2011,8,15,8,15,12,0,pytz.UTC))
        private_entry_g = Entry(title="Secret communication of Guido with space travellers", slug="secret-never-see", status=HIDDEN)
        private_entry_h = Entry(title="Hilda spent her vacation in New Zealand", slug="-k-a-n-g-a-r-o-o-", status=HIDDEN)


        ### NB!
        ### This will fail with an in-memory sqlite3 database, but works fine with an on-disk sqlite3 database. With in-memory database it fails with 'no such table zinnia_category'. If we omit status-PUBLISHED, it works just fine. This is really weird, because the code in a previous test manually queries the database (as sqlite3) and confirms that various Zinnia tables exist, including 'zinnia_category'. Perhaps, Zinnia has some extra functionality when saving PUBLISHED entries, and it does something that breaks with an in-memory database...
        entry.save()
        private_entry_g.save()
        private_entry_h.save()

        # Adding the respective users as authorized. We can only do it after first saving the models.
        private_entry_g.authorized_users.add(user_g)
        private_entry_g.save()
        private_entry_h.authorized_users.add(user_h)
        private_entry_h.save()
        

        # Logging in user_g
        client.login(username='Guido van Rossum', password='3jh3j')
        


        # Now, we did not set the site for the new entries (see django.contrib.sites).
        # Thus, we do not expect them to show up when we follow a direct link.
        # By the way, they still shows up in the dashboard; this is probably a Zinnia issue.
        self.assertEqual(client.get(entry.get_absolute_url()).status_code, 404)
        self.assertEqual(client.get(private_entry_g.get_absolute_url()).status_code, 404)
        self.assertEqual(client.get(private_entry_h.get_absolute_url()).status_code, 404)


        # django.contrib.sites
        # Adding the current site to the Entry.
        # Otherwise it will not be displayed in the detailed view.
        # For some weird reason it is still displayed in the dashboard (that is, zinnia archive of entries). Created an issue for Zinnia on github...
        self.site =  Site.objects.get(pk=settings.SITE_ID)
        entry.sites.add(self.site)
        entry.save()
        private_entry_g.sites.add(self.site)
        private_entry_g.save()
        private_entry_h.sites.add(self.site)
        private_entry_h.save()

        # Test a direct link to the entries. We should see the public entry and the private entry by one of the users
        self.assertContains(client.get(entry.get_absolute_url()), 'wonderful permalink decorator 12321', status_code=200)
#        self.assertContains(client.get(private_entry_g.get_absolute_url()), 'Secret communication of Guido with', status_code=200)
#        self.assertEquals(client.get(private_entry_h.get_absolute_url()).status_code, 404)


        # Also, there should be no link to the hidden entry from the detail view of other entries!
        self.assertNotContains(client.get(entry.get_absolute_url()), private_entry_h.get_absolute_url())
        self.assertNotContains(client.get(private_entry_g.get_absolute_url()), private_entry_h.get_absolute_url())

        # Test the dashboard
        response_dash = client.get(reverse('dashboard'), follow=True)
        self.assertContains(response_dash, 'wonderful permalink decorator 12321', status_code=200)
        self.assertContains(response_dash, 'Secret communication of Guido with', status_code=200)
        self.assertNotContains(response_dash, 'spent her vacation', status_code=200)
        # The dashboard should contain links "Continue Reading" to the visible posts
        self.assertContains(response_dash, entry.get_absolute_url())
#        self.assertContains(response_dash, private_entry_g.get_absolute_url())
#        self.assertNotContains(response_dash, private_entry_h.get_absolute_url())
        
        client.logout()
        # LOG OUT.
        # Still try a direct link to a public entry! But the private one should return 404.
        self.assertContains(client.get(entry.get_absolute_url()), 'wonderful permalink decorator 12321', status_code=200)
        self.assertEquals(client.get(private_entry_g.get_absolute_url()).status_code, 404)
        self.assertEquals(client.get(private_entry_h.get_absolute_url()).status_code, 404)
        # Since we are logged out, the public entry cannot show links to either hidden entry
        self.assertNotContains(client.get(entry.get_absolute_url()), private_entry_g.get_absolute_url())
        self.assertNotContains(client.get(entry.get_absolute_url()), private_entry_h.get_absolute_url())



        # Now logging in user_h
        client.login(username="Hilda von Varden", password="777777777")

        # Test a direct link to the entries. We should see the public entry and the private entry by the other user
        self.assertContains(client.get(entry.get_absolute_url()), 'wonderful permalink decorator 12321', status_code=200)
        self.assertEquals(client.get(private_entry_g.get_absolute_url()).status_code, 404)
        self.assertContains(client.get(private_entry_h.get_absolute_url()), 'Hilda spent her vacation in New Zealand', status_code=200)
        # Also, there should be no link to the hidden entry from the detail view of other entries!
#        self.assertNotContains(client.get(entry.get_absolute_url()), private_entry_g.get_absolute_url())
#        self.assertNotContains(client.get(private_entry_h.get_absolute_url()), private_entry_g.get_absolute_url())


        # Test the dashboard
        response_dash = client.get(reverse('dashboard'), follow=True)
        self.assertContains(response_dash, 'wonderful permalink decorator 12321', status_code=200)
        self.assertNotContains(response_dash, 'Secret communication of Guido with', status_code=200)
        self.assertContains(response_dash, 'spent her vacation', status_code=200)
        # The dashboard should contain links "Continue Reading" to the visible posts
        self.assertContains(response_dash, entry.get_absolute_url())
#        self.assertNotContains(response_dash, private_entry_g.get_absolute_url())
#        self.assertContains(response_dash, private_entry_h.get_absolute_url())
        
        client.logout()
