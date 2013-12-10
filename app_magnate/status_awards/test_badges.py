from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user
from brabeion import badges

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


    
badges.register(TestLikesBadge_0)
