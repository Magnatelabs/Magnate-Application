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
        BadgeAward.objects.create(user=user, slug='horse', level=4)
        BadgeAward.objects.create(user=user, slug='donated-something', level=0)

        from . import award_badges
        # Because we created the badges in an articificial way, the signals would not have triggered
        # No metabadges so far
        self.assertEquals(0, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))

        # Artificially trigger... (NOT TESTING SIGNALS THOUGH)
        award_badges("badge_awarded_horse", user)
        award_badges("badge_awarded_donated-something", user)

         # No metabadges so far; level 4 is not enough
        self.assertEquals(0, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))
        BadgeAward.objects.create(user=user, slug='horse', level=5)
        
        # No metabadges so far
        self.assertEquals(0, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))

        # Artificially trigger... (NOT TESTING SIGNALS THOUGH)
        award_badges("badge_awarded_horse", user)
        award_badges("badge_awarded_donated-something", user)

        # Now the user should have received 2 meta badges:
        # The Spiderman badges and the SuperSpiderman (for receiving the Spiderman)
        self.assertEquals(2, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()])), "Should have received 2 metabadges by now: the Spiderman and the SuperSpiderman (for receiving the Spiderman badge)"
        l = BadgeAward.objects.all()
        self.assertEquals(len(l), 5)
        self.assertTrue(all(user==b.user for b in l))
        
        # Add badges on missing levels
        for i in range(4):
            BadgeAward.objects.create(user=user, slug='horse', level=i)
            award_badges("badge_awarded", user)
            # Nothing should've changed; 2 meta badges
            self.assertEquals(2, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))
            l = BadgeAward.objects.all()
            self.assertEquals(len(l), 5 + (i+1))
            self.assertTrue(all(user==b.user for b in l))
            for b in l:
                if b.is_metabadge():
                    self.assertTrue(b.slug in ['spiderman-turn-off-the-dark', 'super-spiderman'])
                    self.assertEquals(b.level, 0)
