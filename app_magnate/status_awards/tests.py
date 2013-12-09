from django.test import TestCase
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your tests here.
class BadgeTestCase(TestCase):
    def test_overloaded_model(self):
        from brabeion.models import BadgeAward
        user=User(username='me', password='you')
        user.save()
        slug='horse'
        awarded=7
        extra_kwargs={}
        BadgeAward.objects.create(user=user, slug=slug, level=awarded, **extra_kwargs)
