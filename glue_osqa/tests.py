from django.test import TestCase, Client
from app_magnate.unittest import create_test_user
from django.test.utils import override_settings
from django.contrib.auth.models import User
from forum.models.user import User as ForumUser


# Create your tests here.
class FirstOSQATest(TestCase):
    def testSomething(self):
        from django.conf import settings
        # make sure this setting is defined
        # otherwise it fails in subtle ways.
        # For example, you can get IntegrityError: duplicate key violates unique constraint
        # in prop.save() in forum/models/user.py in __setattr__
        # Because it will use UserProperty.objects.get to see if this property already exists, 
        # but in BaseModel in forum/models/base.py, 
        # objects = CachedManager(). So if some cache configuration is
        # broken... you get the idea. 
        self.assertTrue(hasattr(settings, 'CACHE_MAX_KEY_LENGTH'))


    def testOSQAModels(self):
        from forum.models.question import Question
        result = Question.objects.all().filter_state(delete=False)

        
    def testExtendedUser(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        from forum.models.user import User as ExtendedUser
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(ExtendedUser.objects.count(), 0)

        u = User.objects.create(username='rabbit')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 0)

        from tools import downcastUserToExtendedUser
        eu = downcastUserToExtendedUser(u)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)

        self.assertEqual(ExtendedUser.objects.all()[0], eu)
        self.assertEqual(ExtendedUser.objects.all()[0], downcastUserToExtendedUser(u))

        #reload
        u = User.objects.all()[0]
        eu = ExtendedUser.objects.all()[0]
        
        self.assertEqual(u.pk, eu.pk)
        self.assertEqual(u.username, eu.username)




#@override_settings(MIDDLEWARE_CLASSES=['django.middleware.common.CommonMiddleware',
#                                       'django.contrib.sessions.middleware.SessionMiddleware',
#                                       'django.contrib.auth.middleware.AuthenticationMiddleware',
#                                       'forum.middleware.extended_user.ExtendedUser',
#                                       'forum.middleware.request_utils.RequestUtils'])
class testOSQATemplates(TestCase):
    urls = 'glue_osqa.unittest_urls'

    def test_nodeIndex(self):
        from forum.models.user import User
        u = User.objects.create(username='piglet')
        from forum.models.question import Question
        Question.objects.create(author_id=u.pk)

        self.client = Client()
        r = self.client.get('/osqa_forum/')
        self.assertEqual(r.status_code, 200)


    # Not really testing the whole thing...
    # We can't. See below...
    def test_AskQuestion(self):
        user = create_test_user("Water Cooler", "cooler@water.un", "12621262")
        self.client.login(username='Water Cooler', password='12621262')


        # Anonymous user
        # Because if we were to log in, then we need to have ExtendedUser, 
        # but all middleware is disabled in django.test.Client a.k.a. RequestFactory
        # but then it would fail, because request.user would not contain
        # reputation and other fields

        from zinnia.models.entry import Entry
        from zinnia.managers import PUBLISHED, DRAFT, HIDDEN
        import datetime, pytz

        # No questions about no entry
        r = self.client.get('/osqa_forum/questions/ask/')
        self.assertEqual(r.status_code, 404)

        e=Entry.objects.create(title='Can only ask about public entries', slug='j', start_publication=datetime.datetime(2011,8,15,8,15,12,0,pytz.UTC))

        # No questions about draft entries
        e.status=DRAFT
        e.save()
        r = self.client.get('/osqa_forum/questions/ask/?entry_id=1')
        self.assertEqual(r.status_code, 404)

        # No questions about hidden entries
        e.status=HIDDEN
        e.save()
        r = self.client.get('/osqa_forum/questions/ask/?entry_id=1')
        self.assertEqual(r.status_code, 404)

        # Yes, you can ask about public entries!
        e.status=PUBLISHED
        e.save()
        r = self.client.get('/osqa_forum/questions/ask/?entry_id=1')
        self.assertEqual(r.status_code, 200)

        r = self.client.post('/osqa_forum/questions/ask/?entry_id=1', {'title': '', 'text': 'This is the text of my first question', 'tags': 'first second third'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'errorlist')
        self.assertContains(r, 'This field is required')
        self.assertContains(r, 'please enter a descriptive title for your question')

        # with redirect follow=True
        r = self.client.post('/osqa_forum/questions/ask/?entry_id=1', {'title': 'First question! This is now a legitimate question!.', 'text': 'This is great text.', 'tags': 'good for real'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'errorlist')

        # with redirect follow=True
        r = self.client.post('/osqa_forum/questions/ask/?entry_id=1', {'title': 'Second question! This is a great title.', 'text': '', 'tags': 'good for real'}, follow=True)        
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'errorlist')
        self.assertContains(r, 'This field is required')


        # ask another one
        # with redirect follow=True
        r = self.client.post('/osqa_forum/questions/ask/?entry_id=1', {'title': 'Third question!.', 'text': 'Keeps getting better.', 'tags': 'so good'}, follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, 'errorlist')

        self.assertContains(r, 'First question!')      # was successful
        self.assertNotContains(r, 'Second question!')  # failed
        self.assertContains(r, 'Third question!')      # was successful



class testGlueOSQA(TestCase):
    
    def test_user(self):
        from user import has_user, create_user, create_siteowner, USER_AUTHENTICATED, USER_CREATED, USER_DOES_NOT_EXIST, USER_EXISTS_BUT_WRONG_PASSWORD, USER_AUTHENTICATED_BUT_WRONG_MODEL, USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL
        from forum.models.user import User as ForumUser
        from django.contrib.auth.models import User as DjangoUser
        self.assertEquals(has_user('abc', 'def'), USER_DOES_NOT_EXIST)
        self.assertEquals(create_user('abc', 'def'), USER_CREATED)
        self.assertEquals(create_user('abc', 'def'), USER_AUTHENTICATED)
        self.assertEquals(has_user('abc', 'def'), USER_AUTHENTICATED)
        self.assertEquals(has_user('abc', ''), USER_EXISTS_BUT_WRONG_PASSWORD)

        # the password is not really 'rty', the hash of the password is
        DjangoUser.objects.create(username='qwe', password='rty')
        self.assertEquals(has_user('qwe', 'rty'), USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL)
        self.assertEquals(create_user('qwe', ''), USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL)

        u=DjangoUser.objects.get(username='qwe')
        u.set_password('rty')
        u.save() # now the password is really 'try'

        self.assertEquals(has_user('qwe', 'rty'), USER_AUTHENTICATED_BUT_WRONG_MODEL)
        # Cannot create a new user if there is such a Django User,
        # even if there is no Forum User for this username
        self.assertEquals(create_user('qwe', ''), USER_EXISTS_BUT_WRONG_PASSWORD_AND_WRONG_MODEL)
        self.assertEquals(create_user('qwe', 'rty'), USER_AUTHENTICATED_BUT_WRONG_MODEL)

        
        self.assertRaises(Exception, lambda : create_siteowner('root', 'root'), "too late to create a site owner")
        self.assertEquals(has_user('root', 'root'), USER_DOES_NOT_EXIST)

    def test_siteowner(self):
        from user import *
        user=create_siteowner('root_login', 'root_password')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_siteowner)

        self.assertEquals(has_user('root_login', 'root_password'), USER_AUTHENTICATED)
        self.assertEquals(has_user('root_login', 'sdjiofojsfo'), USER_EXISTS_BUT_WRONG_PASSWORD)