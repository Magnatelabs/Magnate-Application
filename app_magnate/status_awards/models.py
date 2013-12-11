from brabeion.models import BadgeAwardAbstractClass
from dashboard.mixins import PrivatelyPublishedModelMixin
from django.conf import settings
from django.core.urlresolvers import reverse

class MagnateBadgeAward(PrivatelyPublishedModelMixin, BadgeAwardAbstractClass):

    def create_entry_content(self):
        return "Fantastic! You have just been awarded a Badge %s! ... <p> %s" % (self.name, self.description)

    def create_entry_slug(self):
        return 'award'

    def as_html(self):
        image_url = "%sstatus_awards/badge_%s_%d.png" % (settings.STATIC_URL, self.slug, self.level)
        return "<a href=\"%s\"><img src=\"%s\" alt=\"%s\" ></a>" % (reverse('status_award_detail')+'?award=%d' % (self.pk), image_url, self.name)

    class Meta:
        abstract = True
