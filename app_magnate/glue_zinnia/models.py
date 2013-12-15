from django.db import models
from django.utils.translation import ugettext_lazy as _
from zinnia.models.entry import EntryAbstractClass, CoreEntry
from zinnia.managers import PUBLISHED


from django.db.models.query import QuerySet
from django.db.models import Q
from django.db import settings

# From  http://stackoverflow.com/questions/2163151/custom-queryset-and-manager-without-breaking-dry
#
# Now we can write things like zinnia.models.Entry.private.authorized_or_published(self.request.user)
# to get the list of all entries where the current user is included in the list of authorized_users.
#
# Beware: zinnia.models.Entry.private.by_authorized_user(None) will return all entries.
# Thus make sure that somebody is authorized!

class AuthorizedUserMixin(object):
    # Return all entries that are either authorized for a particular user OR published (or both, of course, but we don't expect anyone to set authorized_users for a published entry. All entries meant only for particular users should be HIDDEN.).
    # @user has type django.contrib.auth.get_user_model()
    def authorized_or_published(self, user):
        # Make sure that we are given a real user.
        # Otherwise we risk returning ALL entries, including all hidden ones, instead of those authorized for a particular user.
        assert user.is_authenticated(), "Yes" 

        # FIXME! TODO! Temporary assertions. Can remove if everything is fine.
        for entry in self.filter(authorized_users=user):
            assert user in entry.authorized_users.all(), "Tried to return an entry not authorized for %s" % (str(user))

        return self.filter(Q(authorized_users=user) | Q(status=PUBLISHED))

class AuthorizedUserQuerySet(QuerySet, AuthorizedUserMixin):
    pass


class AuthorizedEntriesManager(models.Manager, AuthorizedUserMixin):
    def get_queryset(self):
        return AuthorizedUserQuerySet(self.model, using=self._db)
#    def get_queryset(self):
#        return super(AuthorizedEntriesManager, self).get_queryset().filter(status==HIDDEN)

    # Retrieve those Zinnia entries where the list of authorized_users includes user.
    # (Parameter "user" has type get_user_model())
    def get_user_queryset(self, user):
        return self.get_queryset().filter(authorized_users=user)

class AuthorizedUsersEntry(models.Model):
    """
    Abstract model class to add relationship
    between the entries and the users authorized to view them.

    If there are none specified, it means that
    everyone can view this entry.
    """
    authorized_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
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

    private = AuthorizedEntriesManager()

    # Users can "like" certain entries. By default, they can like
    # only published entries. They cannot "like" private messages meant
    # only for them, such as "You have been awarded a new badge".
    def show_like_button(self):
        return self.status == PUBLISHED

    # Word limit for private and public entries, respectively
    def blurb_word_limit(self):
        return [settings.MAGNATE_PRIVATE_ENTRY_BLURB_WORD_LIMIT, settings.MAGNATE_PUBLIC_ENTRY_BLURB_WORD_LIMIT][self.status==PUBLISHED]

    def icon_url(self):
        # take the part of the slug until the first dash to determine the type of the post
        # e.g. 'article-about-obama' --> 'article', 'donation-by-joe-bloggs-2384734879' --> 'donation'
        kind = self.slug[:self.slug.find('-')]
        return settings.STATIC_URL + settings.MAGNATE_ICON_BY_ENTRY_TYPE.get(kind, settings.MAGNATE_ICON_BY_ENTRY_TYPE['default'])


    class Meta(CoreEntry.Meta):
        abstract = True

