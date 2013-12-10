from brabeion.base import Badge, BadgeAwarded, BadgeDetail
from social.models import total_likes_by_user
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


    
badges.register(LikesBadge)
