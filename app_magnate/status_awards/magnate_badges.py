from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user
from donations.utils import all_donations_by_user
from brabeion import badges


class LikesBadge(Badge):
    slug="likes"
    levels = [
        BadgeDetail("Bronze-Liker", "Likes a little"),
        BadgeDetail("Silver-Liker", "Likes more"),
        BadgeDetail("Gold-Liker", "Likes a lot"),
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
        BadgeDetail("New Donor", "Donated a lilttle"),
        BadgeDetail("Intermediate Donor", "Donated more"),
        BadgeDetail("Advanced Donor", "Donated a lot "),
        BadgeDetail("Karmic Donor", "Gave away everything")
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

badges.register(LikesBadge)
badges.register(DonorBadge)
