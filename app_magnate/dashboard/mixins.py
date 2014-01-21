from django.db import models
from django.contrib.sites.models import Site
from zinnia.models.entry import Entry
from zinnia.managers import HIDDEN
#from slugify import slugifyx
from django.db import settings

# This mixin is used to make certain model automatically publish a post to the blog on the first save() -- or possibly later if the post hasn't been published yet because of some error. Example: badges, donations. After you make a donation, you want to see a post about it. After you are awarded a badge, you want to see a post about it. Then, for example, a picture with a badge could link to this post...

#
# The decorated model MUST have a field called "user".
class PrivatelyPublishedModelMixin(models.Model):
    # Private entry (blog post) noifying the user about a  donation, badge, etc.
    entry = models.OneToOneField(Entry,) # related_name='object_reason_for_post')

    # Override this method to auto-generate meaningful titles for automated posts
    def create_entry_title(self):
        return 'Entry title You have a new %s' % (str(self.__class__).split("'")[1])

    # Override this method to auto-generate meaningful content
    def create_entry_content(self):
        return 'Entry content You have a new %s' % (str(self.__class__).split("'")[1])
        
    # Override this to specify a meaningul slug. It does not have to be unique, as this mixin will append to the slug the id (primary key) of the entry.
    def create_entry_slug(self):
        return str(self.__class__).split("'")[1]

    # QUESTION. Do we want sql transactions?
    # or is it OK to save an object(badge, donation) if saving a related blog post fails? 
    # In this case, do we want later to retry posting the same thing?
    #
    # Though I am not sure we can even have transactions here, because to add a site (django.contrib.sites) to an Entry we have to initially save it first
    def save(self, *args, **kwargs):
        if self.pk is None: # or if there is no entry? What is a good check?
            # take action on first save
            # NB! Try to make sure that the slug is unique so we can have separate links to separate messages
            entry=Entry(title=self.create_entry_title(), content=self.create_entry_content(), status=HIDDEN,) 
            entry.save()
            entry.slug=self.create_entry_slug() + '-' + str(entry.pk)
            entry.sites.add(Site.objects.get(pk=settings.SITE_ID))
            entry.authorized_users.add(self.user)
            entry.save()
            # Should we perhaps save somewhere this Site.objects.get(pk=settings.SITE_ID) so we don't have to query it every time? Though, I guess, it is not such a big deal here, as we are rarely saving things that have associated blog posts. We are not generating blog posts (entries) every second...
            self.entry=entry
        else:
            if self.entry is None:
                pass # QUESTION. Should we still post? Better late than never? Though, with transactions, we'd never get here.
            
        super(PrivatelyPublishedModelMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
