from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user, total_ratings_by_user
from donations.utils import total_donation_amount, all_donations_by_user
from brabeion import badges
from .base import MetaBadge

class TestLikesBadge_0(Badge):
    slug="horse"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
        "Cream",
        "Vanilla",
        "Chocolate",
        "Merengue",
        BadgeDetail("Salsa", "The best badge ever"),
        "Development",
        "Synergy"
    ]

    events = [
        "user_liked_entry",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        likes = total_likes_by_user(user)
        if likes >= 7:
            return BadgeAwarded(5) # skip a level to make it more interesting
        if likes >= 5:
            return BadgeAwarded(3)
        elif likes >= 2:
            return BadgeAwarded(2)
        elif likes >= 1:
            return BadgeAwarded(1)



class DonatedSomethingTestBadge(Badge):
    slug="donated-something"
    levels = [
        BadgeDetail("Nice person!", "This badge is given for any donation"),
    ]
    events = [
        "donation",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        assert (len(all_donations_by_user(user))==0) == (total_donation_amount(user)==0), "Total donation amount is zero if and only if there are no donations"
        if total_donation_amount(user) > 0:
            return BadgeAwarded(1)



class Spiderman(MetaBadge):
    slug="spiderman-turn-off-the-dark"
    levels = [
        BadgeDetail("Spiderman", "Turn off the dark."),
    ]
    requirements = [
        { 'horse' : 5, 'donated-something' : 0 }
    ]
    events = ['badge_awarded_'+s for s in set(s for s_l in requirements for s in s_l.keys())]


    assert len(events)==2
    assert 'badge_awarded_horse' in events
    assert 'badge_awarded_donated-something' in events



class SuperSpiderman(MetaBadge):
    slug='super-spiderman'
    levels = [
        BadgeDetail("Simple", "Today"),
        BadgeDetail("Super", "Tomorrow"),
    ]
    requirements = [
        { 'spiderman-turn-off-the-dark' : 0 },
        { 'horse' : 8 }
    ]

    events = ['badge_awarded_'+s for s in set(s for s_l in requirements for s in s_l.keys())]

    assert len(events)==2
    assert 'badge_awarded_horse' in events
    assert 'badge_awarded_spiderman-turn-off-the-dark' in events


class FearlessRaterBadge(Badge):
    slug='fearless-rater'
    levels = [
        BadgeDetail("Rate-One", "Yes"),
        BadgeDetail("Rate-Two", "Maybe"),
    ]
    events = [
        "user_rated_something"
    ]
    multiple = False

    def award(self, **state):
        user=state["user"]
        ratings = total_ratings_by_user(user)
        if ratings >= 2:
            return BadgeAwarded(2)
        elif ratings >= 1:
            return BadgeAwarded(1)
        

assert badges._registry=={}

badges.register(TestLikesBadge_0)

assert(len(badges._registry) == 1)
assert isinstance(badges._registry[TestLikesBadge_0.slug], TestLikesBadge_0)

badges.register(DonatedSomethingTestBadge)

assert(len(badges._registry) == 2)
assert isinstance(badges._registry[TestLikesBadge_0.slug], TestLikesBadge_0)
assert isinstance(badges._registry[DonatedSomethingTestBadge.slug], DonatedSomethingTestBadge)

badges.register(FearlessRaterBadge)
assert(len(badges._registry) == 3)
assert isinstance(badges._registry[TestLikesBadge_0.slug], TestLikesBadge_0)
assert isinstance(badges._registry[DonatedSomethingTestBadge.slug], DonatedSomethingTestBadge)
assert isinstance(badges._registry[FearlessRaterBadge.slug], FearlessRaterBadge)

# Purposely first registering SuperSpiderman, to make it trickier
# SuperSpiderman should be awarded whenever Spiderman is awarded
badges.register(SuperSpiderman)
badges.register(Spiderman)

assert(len(badges._registry) == 5)
assert isinstance(badges._registry[TestLikesBadge_0.slug], TestLikesBadge_0)
assert isinstance(badges._registry[DonatedSomethingTestBadge.slug], DonatedSomethingTestBadge)
assert isinstance(badges._registry[FearlessRaterBadge.slug], FearlessRaterBadge)
assert isinstance(badges._registry[SuperSpiderman.slug], SuperSpiderman)
assert isinstance(badges._registry[Spiderman.slug], Spiderman)
