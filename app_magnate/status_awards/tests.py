from django.test import TestCase
from django.contrib.auth import get_user_model
User=get_user_model()
from brabeion.models import BadgeAward


# Create your tests here.
class BadgeAwardTestCase(TestCase):
    def test_overloaded_model(self):

        user=User(username='me', password='you')
        user.save()
        slug='horse'
        awarded=7
        extra_kwargs={}
        ba=BadgeAward.objects.create(user=user, slug=slug, level=awarded, **extra_kwargs)
        # Badge slug and level determine name and description
        self.assertEqual(ba.name, "Salsa")
        self.assertEqual(ba.description, "The best badge ever")

        # A new Entry should have been created for this BadgeAward
        entry = ba.entry
        self.assertEquals(entry.title, "You have a new brabeion.models.BadgeAward")
        self.assertEqual(entry.slug, "badge-1")
        self.assertEqual(entry.content, 'Fantastic! You have just been awarded a Badge Salsa! ... <p> The best badge ever')

    def test_metabadge(self):
        user=User(username='she', password='is here')
        user.save()
        BadgeAward.objects.create(user=user, slug='horse', level=8)
        BadgeAward.objects.create(user=user, slug='donated-something', level=0)

        from . import award_badges
        award_badges("badge_awarded", user)
        # Now the user should have receive 1 meta badge
        self.assertEquals(1, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))
        
