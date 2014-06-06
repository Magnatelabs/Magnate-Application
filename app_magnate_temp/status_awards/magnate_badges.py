from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user, total_ratings_by_user
from donations.utils import all_donations_by_user
from brabeion import badges
from .base import MetaBadge

class LikesBadge(Badge):
    slug="likes"
    levels = [
        BadgeDetail("Finger Painting Badge", "Your very first Magnte Mark--this one is going on the fridge"),
        BadgeDetail("Crayon Badge", "An upgrade from finger paints! Just try your best to keep all Magnate Marks within the lines"),
        BadgeDetail("Colored Pencil Badge", "Crayons be damned. You express your opinions at a toddler's level"),

#        BadgeDetail("Bronze-Liker", "Likes a little"),
#        BadgeDetail("Silver-Liker", "Likes more"),
#        BadgeDetail("Gold-Liker", "Likes a lot"),
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



class DonorBadge(Badge):
    slug="donor"
    levels = [
        BadgeDetail("New Donor Badge", "Some skin is now in the game. You are a bona fide member of the Magnate community"),
        BadgeDetail("Intermediate Donor Badge", "A second donation? Wow, you just upped the game"),
        BadgeDetail("Organ Donor Badge", "Hand over the card, Magnate is now a serious part of your life"),
        BadgeDetail("Karmic Donor Badge", "Give away everything")

#        BadgeDetail("New Donor", "Donated a lilttle"),
#        BadgeDetail("Intermediate Donor", "Donated more"),
#        BadgeDetail("Advanced Donor", "Donated a lot "),
#        BadgeDetail("Karmic Donor", "Gave away everything")
    ]
    events = [
        "user_donation",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        donations = all_donations_by_user(user)
        count = len(donations)
        amount = sum([d.amount for d in donations])
        if (amount > 10000):
            return BadgeAwarded(4)            # Note that conditions on different levels are not monotonous
        elif (count > 4) and (amount > 500):  # Expected behavior? Do you need lower level to qualify for higher?
            return BadgeAwarded(3)            # Probably not... But once you qualify for higher, you 
        elif (count > 2) and (amount > 100):  # won't get the lower ones ;-)
            return BadgeAwarded(2)
        elif (count > 0) and (amount > 0):
            return BadgeAwarded(1)

class RaterBadge(Badge):
    slug='rater'
    levels = [
        BadgeDetail("Nooby Tester Badge", "Cleaning Magnate bugs through rating"),
        BadgeDetail("Gold Nooby Tester Badge", "A little spring cleaning only helps Magnate"),
        BadgeDetail("Alpha Tester Badge", "Rated a lot"),
        BadgeDetail("Beta Tester Badge", "Rated everything"),

#        BadgeDetail("Bronze Rater", "Rated a little"),
#        BadgeDetail("Silver Rater", "Rated some more"),
#        BadgeDetail("Gold Rater", "Rated a lot"),
#        BadgeDetail("Platinum Rater", "Rated everything"),        
    ]
    events = [
        "user_rated_something"
    ]
    multiple = False

    def award(self, **state):
        user=state["user"]
        ratings = total_ratings_by_user(user)
        if ratings >= 10:
            return BadgeAwarded(4)
        elif ratings >= 5:
            return BadgeAwarded(3)
        elif ratings >= 2:
            return BadgeAwarded(2)
        elif ratings >= 1:
            return BadgeAwarded(1)

class MemeMagnate(MetaBadge):
    slug="meme_magnate"
    levels = [
        BadgeDetail("Meme Magnate", "Slowly learning to be a magnate..."),
    ]
    requirements = [
        { 'likes' : 0, 'donor' : 0 }
    ]
    events = ['badge_awarded_'+s for s in set(s for s_l in requirements for s in s_l.keys())]

class FavouriteMagnate(MetaBadge):
    slug='favourite'
    levels = [
        BadgeDetail("Starter Magnate", "Good job, but it's kind of easy to earn this one..."),
        BadgeDetail("Favourite Magnate", "Given after you win Meme Magnate and Favourite Magnate"),
    ]
    requirements = [
        { 'rater' : 0, 'donor' : 0 },
        { 'favourite' : 0, 'meme_magnate' : 0 },
    ]
    events = ['badge_awarded_'+s for s in set(s for s_l in requirements for s in s_l.keys())]

badges.register(LikesBadge)
badges.register(DonorBadge)
badges.register(RaterBadge)
badges.register(MemeMagnate)
badges.register(FavouriteMagnate)
