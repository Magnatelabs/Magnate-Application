# importing will register the badges
import magnate_badges



# @event --- string describing what happened, e.g. "points_awarded" or "user_liked_something".
# Every Badge is listening for certain events that may trigger an award.
def award_badges(event, user):
    from brabeion import badges
    badges.possibly_award_badge(event, user=user)    
    

