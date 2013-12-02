from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from zinnia.models.entry import EntryAbstractClass, CoreEntry


class AuthorizedUsersEntry(models.Model):
    """
    Abstract model class to add relationship
    between the entries and the users authorized to view them.

    If there are none specified, it means that
    everyone can view this entry.
    """
    authorized_users = models.ManyToManyField(
        get_user_model(),
        related_name='authorized_entries',
        blank=True, null=False,
        verbose_name=_('authorized users'))

    class Meta:
        abstract = True


# We are extending Zinnia's EntryAbstractClass.
# Now we will set e.g. ZINNIA_ENTRY_BASE_MODEL= 'models.EntryCheck' in settings.py
class EntryCheck(
        EntryAbstractClass,
        AuthorizedUsersEntry,):

    def __unicode__(self):
        return u'EntryCheck %s' % self.title

    class Meta(CoreEntry.Meta):
        abstract = True

