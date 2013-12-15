from brabeion.signals import badge_awarded
from django.dispatch import receiver

from django.conf import settings
if not settings.TESTING:
    # importing will register the badges
    import magnate_badges
else:
    import test_badges


# @event --- string describing what happened, e.g. "points_awarded" or "user_liked_something".
# Every Badge is listening for certain events that may trigger an award.
def award_badges(event, user):
    assert isinstance(event, str)        
    from brabeion import badges
    badges.possibly_award_badge(event, user=user)    




# Every time a badge is awarded, may need to award metabadges
@receiver(badge_awarded)
def on_badge_awarded(sender, **kwargs):
#    print 'badge_awarded_' + sender.slug
    award_badges('badge_awarded_' + sender.slug, user=kwargs['badge_award'].user)
