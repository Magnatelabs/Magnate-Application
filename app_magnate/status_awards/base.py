from brabeion.base import Badge, BadgeAwarded
from brabeion.models import BadgeAward
from django.db.models import Max

# a badge given for collecting other badges
class MetaBadge(Badge):
    events = [
        "badge_awarded"
    ]
    multiple = False

    def award(self, **state):
        user=state["user"]
        
        # Returns the highest level achieved by this user for each badge slug, as a dictionary {slug : max_level} 
        achieved = {x['slug'] : x['max_level'] for x in BadgeAward.objects.filter(user=user).values('slug').annotate(max_level=Max('level'))}

        for i, r in enumerate(self.requirements):
            if not all([achieved[slug] >= r[slug] for slug in r]):
                if i > 0:
                    return BadgeAwarded(i)
                else:
                    return
        return BadgeAwarded(len(self.requirements))

 
