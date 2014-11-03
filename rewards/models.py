from django.db import models
from dashboard.mixins import PrivatelyPublishedModelMixin
from django.conf import settings
from forum.models.utils import PickledObjectField
from forum.models.action import ActionProxyMetaClass
import re

SCHEDULED = 0
ACTIVE = 1
SUSPENDED = 2
CANCELED = 3
COMPLETED = 4

FUNDRAISER_LOGO_IMAGES = 'uploads/fundraiser_logos'

class AgendaManager(models.Manager):
    def get_queryset(self):
        qs = super(AgendaManager, self).get_queryset()
        if self.model is not Agenda:
            return qs.filter(agenda_type = self.model.get_type())
        else:
            return qs

class Agenda(PrivatelyPublishedModelMixin, models.Model):
    STATUS_CHOICES = ((SCHEDULED, 'scheduled'),
                      (ACTIVE, 'active'),
                      (SUSPENDED, 'suspended'),
                      (CANCELED, 'canceled'),
                      (COMPLETED, 'completed'),)


    # the user who created the event
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    agenda_type = models.CharField(max_length=32)

    # when the event starts and/or when is the deadline
    date = models.DateTimeField()
    status = models.IntegerField(
        'status', choices=STATUS_CHOICES, default=SCHEDULED)

    # arbitrary comments; probably the name of the event
    # this is for admin use only; this will NOT be published to the users
    admin_note = models.CharField(max_length=200)

    extra = PickledObjectField(blank=True)


    objects = AgendaManager()

    # added for the Lobby opportunities page
    title = models.CharField(max_length=200)
    image = models.ImageField('fundraiser_logo', blank=True, upload_to=FUNDRAISER_LOGO_IMAGES)

    def __unicode__(self):
        return '%s %s (event by %s on %s)' % (self.__class__.__name__, self.admin_note, self.user, self.date)

    @classmethod
    def get_type(cls):
        return re.sub(r'agenda$', '', cls.__name__.lower())

    #Hack to help fundraising content fit into Lobbies
    def as_fundraising_agenda(self):
        self.__class__ = FundraisingAgenda
        return self

    #override
    def create_entry_title(self):
        return '%s (EDIT THIS!)' % (self.admin_note)

    #override
    def create_entry_content(self):
        return '%s. The event will take place on %s. This entry is hidden. Edit it to describe the event, add pictures, etc. See how it looks on your own dashboard. However, you are the only one who can see it. When you are ready, set the status to PUBLISHED so other users can see it as well. Lastly, do not confuse the timestamp of this entry with the start time of the actual event.' % (self.admin_note, self.date)

    #override 
    def create_entry_slug(self):
        return self.agenda_type

    def defaultExtra(self):
        return None

    def save(self, *args, **kwargs):
        isnew = False

        if not self.id:
            self.agenda_type = self.__class__.get_type()
            isnew = True
            self.extra = self.defaultExtra()

        super(Agenda, self).save(*args, **kwargs)




class AgendaProxy(Agenda):
    # ActionProxyMetaClass works for us. We just need to make
    # sure that everything inheriting from AgendaProxy is still a 
    # proxy model; that's all.
    __metaclass__ = ActionProxyMetaClass

    class Meta:
        proxy = True

# The users also get rewarded in this way: they are invited to a hangout.
#
# Using PrivatelyPublishedModelMixin, so the new hangout will automatically
# get a Zinnia entry. After it is edited, the admin should set its
# visibility to PUBLIC.
class HangoutAgenda(AgendaProxy):

    def __unicode__(self):
        return '%s (hosted by %s on %s)' % (self.admin_note, self.user, self.date)

#    #override
#    def create_entry_title(self):
#        return '%s (EDIT THIS!)' % (self.admin_note)

#    #override
#    def create_entry_content(self):
#        return '%s. The event will take place on %s. This entry is hidden. Edit it to describe the event, add pictures, etc. See how it looks on your own dashboard. However, you are the only one who can see it. When you are ready, set the status to PUBLISHED so other users can see it as well. Lastly, do not confuse the timestamp of this entry with the start time of the actual event.' % (self.admin_note, self.date)


    def is_completed(self):
        return self.status == COMPLETED

class FundraisingAgenda(AgendaProxy):

    # collected_amount, target_amount are stored in extra

    def defaultExtra(self):
        return { 'current-amount': 0,
                 'target-amount':  0  }

    # Convenience methods for the templates.
    def current_amount(self):
        return self.extra['current-amount']

    def target_amount(self):
        return self.extra['target-amount']


    def target_reached(self):
        return float(self.current_amount()) >= float(self.target_amount())
        
    def __unicode__(self):
        return '%s (hosted by %s on %s)' % (self.admin_note, self.user, self.date)
