from django.test import TestCase
from django.contrib.auth import get_user_model
User=get_user_model()

# Create your tests here.
class BadgeAwardTestCase(TestCase):
    def test_overloaded_model(self):
        from brabeion.models import BadgeAward
        user=User(username='me', password='you')
        user.save()
        slug='horse'
        awarded=7
        extra_kwargs={}
        ba=BadgeAward.objects.create(user=user, slug=slug, level=awarded, **extra_kwargs)

        # A new Entry should have been created for this BadgeAward
        entry = ba.entry
        self.assertEquals(entry.title, "You have a new brabeion.models.BadgeAward")
        self.assertEqual(entry.slug, "brabeion.models.BadgeAward-1")
        self.assertEqual(entry.content, "You have a new brabeion.models.BadgeAward")
        
