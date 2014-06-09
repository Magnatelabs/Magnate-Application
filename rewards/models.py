from django.db import models
from dashboard.mixins import PrivatelyPublishedModelMixin
from django.conf import settings

# The users also get rewarded in this way: they are invited to a hangout.
#
# Using PrivatelyPublishedModelMixin, so the new hangout will automatically
# get a Zinnia entry. After it is edited, the admin should set its
# visibility to PUBLIC.
class Hangout(PrivatelyPublishedModelMixin, models.Model):
    # the user who created the event
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    # when the event starts
    date = models.DateTimeField()

    # arbitrary comments; probably the name of the event
    # this is for admin use only; this will NOT be published to the users
    admin_note = models.CharField(max_length=200)


    def __unicode__(self):
        return '%s (hosted by %s on %s)' % (self.admin_note, self.user, self.date)

    #override
    def create_entry_title(self):
        return '%s (EDIT THIS!)' % (self.admin_note)

    #override
    def create_entry_content(self):
        return '%s. The event will take place on %s. Make the associated entry PUBLIC to publish it on the website.' % (self.admin_note, self.date)

    #override 
    def create_entry_slug(self):
        return 'hangout'


