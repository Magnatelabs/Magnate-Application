from brabeion.models import BadgeAwardAbstractClass
from dashboard.mixins import PrivatelyPublishedModelMixin

class MagnateBadgeAward(PrivatelyPublishedModelMixin, BadgeAwardAbstractClass):
    class Meta:
        abstract = True
