"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from app_magnate.unittest import create_test_user
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import StudyModel

class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = create_test_user('temporary', 'temporary@gmail.com', 
'temporary')
        self.client.login(username='temporary', password='temporary')


    startup = {
        'entity': 'Contextuall', 
        'entity_url': 'https://contextuall.com', 
        'industry': 'other', 
        'description': 'What would you do differently if you could predict the future?'
    }
    def test_submit_startup(self):
        c = self.client
    	r=c.get(reverse('study_index'))
    	self.assertEquals(r.status_code, 200)
    	# Pretend we have found a cool startup and want to suggest it to Magnate

        # incorrect submission: not enough info
        r=c.post(reverse('study_index'), {'entity': 'Google', 'industry': 'social-network'})
        self.assertEquals(r.status_code, 200)
        self.assertTrue('Your information was not entered correctly' in r.content)

    	r=c.post(reverse('study_index'), self.startup, follow=True)

#    	self.assertEquals(r.status_code, 302)
#        url_next=r._headers['location'][1] 
#        r=c.get(url_next)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(len(StudyModel.objects.all()), 1)

        sm = StudyModel.objects.all()[0]
        for field in self.startup:
            self.assertEquals(getattr(sm, field), self.startup[field])
        self.assertFalse(sm.docfile) # no file


        from forum.models.action import Action
        act = Action.objects.all()[0]
        self.assertEquals(act.action_type, 'proposecompany')
        self.assertEquals(act.extra, sm)
