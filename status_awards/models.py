from brabeion.models import BadgeAwardAbstractClass
from dashboard.mixins import PrivatelyPublishedModelMixin

from forum.actions.node import AskAction, AnswerAction
from forum.actions.meta import VoteUpAction, VoteDownAction
from donations.models import DonationAction
from django.db.models.signals import post_save


class MagnateBadgeAward(PrivatelyPublishedModelMixin, BadgeAwardAbstractClass):

    def create_entry_content(self):
        return "Fantastic! You have just been awarded the %s! ... <p> %s" % (self.name, self.description)

    def create_entry_slug(self):
        return 'badge'

    # Metabadges are special badges that are awarded for receiving other badges
    def is_metabadge(self):
        from .base import MetaBadge
        return isinstance(self._badge, MetaBadge)

    class Meta:
        abstract = True


# When a new osqa Action is saved, let's see if we need to award any badges.
# Note that all supported actions such as AskAction have to be explicitly
# connected below. In this case badges dependent on this action would subscribe
# for the event 'ask' (lowercased AskAction without the 'action') - that's what
# OSQA does. Try "SELECT * from forum_action" to get some ideas.
def onActionSave(sender, **kwargs):
    # sender.get_type() == kwargs['instance'].get_type() is 'ask' for AskAction, etc.
    # just "SELECT * from forum_action" and see what is available.
    # And if you want some other actions, remember to connect the signals below.
    if kwargs.get('created', False):
      user = kwargs['instance'].user
      from . import award_badges
      award_badges(sender.get_type(), user)

post_save.connect(onActionSave, sender=AskAction)
post_save.connect(onActionSave, sender=AnswerAction)
post_save.connect(onActionSave, sender=VoteUpAction)
post_save.connect(onActionSave, sender=VoteDownAction)
post_save.connect(onActionSave, sender=DonationAction)