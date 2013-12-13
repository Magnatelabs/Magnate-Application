from brabeion.models import BadgeAwardAbstractClass
from dashboard.mixins import PrivatelyPublishedModelMixin



class MagnateBadgeAward(PrivatelyPublishedModelMixin, BadgeAwardAbstractClass):

    def create_entry_content(self):
        return "Fantastic! You have just been awarded a Badge %s! ... <p> %s" % (self.name, self.description)

    def create_entry_slug(self):
        return 'badge'

    # Metabadges are special badges that are awarded for receiving other badges
    def is_metabadge(self):
        from .base import MetaBadge
        return isinstance(self._badge, MetaBadge)

    class Meta:
        abstract = True

