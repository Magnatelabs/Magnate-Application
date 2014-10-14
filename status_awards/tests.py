from django.test import TestCase
#from django.contrib.auth import get_user_model
#User=get_user_model()
#from forum.models.user import User
from brabeion.models import BadgeAward

from zinnia.models.entry import Entry

from random import randrange, random, seed
from social.models import toggle_like_unlike, total_likes_by_user, Like
from donations.models import Donation
import math
from . import award_badges
from app_magnate.unittest import create_test_user
from django.test.client import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class BadgeAwardTestCase(TestCase):
#    from forum.models.user import User as ForumUser

# Running the tests with the standard user model
# After that rerunning all the same tests with forum.models.User,
# our custom user model that is inherited from the standard one.
#
# This is done by inheriting from BadgeAwardTestCase and 
# overriding User.
    from django.contrib.auth import get_user_model
    User = get_user_model()

    def test_overloaded_model(self):

        user=self.User(username='me', password='you')
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
        self.assertEquals(entry.title, "You have just won a new badge!")
        self.assertEqual(entry.slug, "badge-1")
        self.assertEqual(entry.content, 'Fantastic! You have just been awarded the Salsa! ... <p> The best badge ever')


    def test_nonexistent(self):
        user=create_test_user('she', 'she@is.here', 'is here')
        user.save()
        from brabeion import badges
        # hack: fake the existence of this badge so an object can be created
        # simulating the situation where some badges were awarded, then a particular
        # badge was removed (in principle), but the previously awarded badges still
        # persist in the database
        badges._registry['thereisnosuchbadge']=badges._registry['horse']
        b=BadgeAward.objects.create(user=user, slug='thereisnosuchbadge', level=0)
        del badges._registry['thereisnosuchbadge']
        c = Client()
        self.assertTrue(c.login(username='she', password='is here'))
        response = c.get(reverse('dashboard'), follow=True)

    def test_metabadge(self):
        user=self.User(username='she', password='is here')
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
        # Checking username equality, not user objects themselves
        # Because we may have a custom user model
        self.assertTrue(all(user.username==b.user.username for b in l))
        
        # Add badges on missing levels
        for i in range(4):
            BadgeAward.objects.create(user=user, slug='horse', level=i)
            award_badges("badge_awarded", user)
            # Nothing should've changed; 2 meta badges
            self.assertEquals(2, sum([1 for b in BadgeAward.objects.all() if b.is_metabadge()]))
            l = BadgeAward.objects.all()
            self.assertEquals(len(l), 5 + (i+1))
            # Checking username equality, not user objects themselves
            # Because we may have a custom user model
            self.assertTrue(all(user.username==b.user.username for b in l))
            for b in l:
                if b.is_metabadge():
                    self.assertTrue(b.slug in ['spiderman-turn-off-the-dark', 'super-spiderman'])
                    self.assertEquals(b.level, 0)


    def setUp(self):
        for i in range(10):
            self.User.objects.create(username='user'+str(i), password=str(i))   

    def setup(self, nu): # not setUp; calling it manually
        seed(32847+nu)

        self.nu=nu
        self.users=[]
        for i in range(self.nu):
            user=self.User.objects.get(username=('user'+str(i)))
            self.users.append(user)

        self.ne=10
        self.entries=[]
        for i in range(self.ne):
            entry=Entry.objects.create(title='Entry' + str(i), content=str(i) + '___ content ---')
            self.entries.append(entry)
        
        self.total_donation = [0.0] * self.nu
        self.max_total_likes = [0] * self.nu

    def teardown(self): # not tearDown(); calling it manually
        Like.objects.all().delete()
        BadgeAward.objects.all().delete()
        Donation.objects.all().delete()

    def do_many(self, n_users, n_repetitions):
        self.setup(n_users)
        for r in range(n_repetitions):
            u_ind=randrange(self.nu)
            user=self.users[u_ind]
            if randrange(2)==0: # like/unlike something
                e_ind=randrange(self.ne)
                entry=self.entries[e_ind]
                toggle_like_unlike(entry, user)
                # We still need to call award_badges
                # But only for regular badges, not for metabadges
                # If you decide to award badges on signal, try making award_badges do nothing and run the tests
                award_badges("user_liked_entry", user)
            else: # donate something
                amount = 0.1*math.exp(random()*10) # make it fluctuate a lot
                Donation.objects.create(user=user, amount=amount)
                self.total_donation[u_ind] += amount
                # We still need to call award_badges
                # But only for regular badges, not for metabadges
                # If you decide to award badges on signal, try making award_badges do nothing and run the tests
                award_badges("donation", user)

            for i in range(self.nu):
                user=self.users[i]
                tl = total_likes_by_user(user)
                # max total likes this user had during this test, given that it is possible to unlike entries
                self.max_total_likes[i] = max(self.max_total_likes[i], tl)
                # What matters is how many likes the user had at some moment, as this would determine whether the user should have received a badge or not. The user is free to unlike entries after receiving a badge; he will still keep the badge.
                mtl = self.max_total_likes[i]
                td = self.total_donation[i]
                expected=[]
                if (mtl >= 1):
                    expected.append(('horse', 0))
                if (mtl >= 2):
                    expected.append(('horse', 1))
                if (mtl >= 5):
                    expected.append(('horse', 2))
                if (mtl >= 7):
                    expected.append(('horse', 4))
                if (td > 0):
                    expected.append(('donated-something', 0))
                if (('horse', 5) in expected) and (('donated-something', 0) in expected):
                    expected.append(('spiderman-turn-off-the-dark', 0))
                    expected.append(('super-spiderman', 0))
                if ('horse', 8) in expected:
                    expected.append(('super-spiderman', 1))
                # the first check is redundant
                self.assertEquals(len(expected), len(user.badges_earned.all()))
                self.assertEquals(set(expected), set((b.slug, b.level) for b in user.badges_earned.all()))

            # the first check is again redundant
            # total number of badges = sum of total number of badges earned by each user
            self.assertEquals(sum([len(user.badges_earned.all()) for user in self.users]), len(BadgeAward.objects.all()))
            # now compare the set of all badges to the union of the sets of badges awarded to each user
            self.assertEquals(set([b for user in self.users for b in user.badges_earned.all()]), set(BadgeAward.objects.all()))
        self.teardown()


    def test_several(self):
        self.do_many(3, 10)
        self.do_many(2, 50)
        self.do_many(1, 30)
        self.do_many(5, 50) 


class BadgeAwardTestCaseWithForumUserModel(BadgeAwardTestCase):
    from forum.models.user import User as ForumUser
    User=ForumUser

