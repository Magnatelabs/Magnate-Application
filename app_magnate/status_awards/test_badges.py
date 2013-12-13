from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user
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
        "user_donation",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        assert (len(all_donations_by_user(user))==0) == (total_donation_amount(user)==0), "Total donation amount is zero if and only if there are no donations"
        if total_donation_amount(user) > 0:
            print "giving badge"
            return BadgeAwarded(1)



class Spiderman(MetaBadge):
    slug="spiderman-turn-off-the-dark"
    levels = [
        BadgeDetail("Spiderman", "Turn off the dark."),
    ]
    requirements = [
        { 'horse' : 8, 'donated-something' : 0 }
    ]

    
badges.register(TestLikesBadge_0)
badges.register(DonatedSomethingTestBadge)
badges.register(Spiderman)
