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
