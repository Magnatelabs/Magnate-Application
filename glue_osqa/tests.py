from django.test import TestCase, Client

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
        downcastUserToExtendedUser(u)

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(ExtendedUser.objects.count(), 1)

        #reload
        u = User.objects.all()[0]
        eu = ExtendedUser.objects.all()[0]
        
        self.assertEqual(u.pk, eu.pk)
        self.assertEqual(u.username, eu.username)




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

        # Anonymous user
        # Because if we were to log in, then we need to have ExtendedUser, 
        # but all middleware is disabled in django.test.Client a.k.a. RequestFactory
        # but then it would fail, because request.user would not contain
        # reputation and other fields


        r = self.client.get('/osqa_forum/questions/ask/')
        self.assertEqual(r.status_code, 200)

        r = self.client.post('/osqa_forum/questions/ask/', {'title': '', 'text': 'This is the text of my first question', 'tags': 'first second third'})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'errorlist')
        self.assertContains(r, 'This field is required')
        self.assertContains(r, 'please enter a descriptive title for your question')

        r = self.client.post('/osqa_forum/questions/ask/', {'title': 'Now this is a legitimate question.', 'text': '', 'tags': 'good for real'})
        
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'errorlist')
        # Because the user is anonymous, will require recaptcha!
