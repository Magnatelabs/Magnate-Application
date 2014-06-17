from django.test import TestCase

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

