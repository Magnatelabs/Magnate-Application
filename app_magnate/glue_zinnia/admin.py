from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin

from glue_zinnia.models import AuthorizedEntry


from zinnia.admin.forms import EntryAdminForm
class AuthorizedEntryAdminForm(EntryAdminForm):
    class Meta:
        model=AuthorizedEntry

class AuthorizedEntryAdmin(EntryAdmin):
  form=AuthorizedEntryAdminForm
  # In our case we put the gallery field
  # into the 'Content' fieldset
#  print '!!!'
#  print EntryAdmin.fieldsets[2]
#  print EntryAdmin.filter_horizontal
  fieldsets = EntryAdmin.fieldsets[:2] + ((_('Privacy'), {'fields': (
      'login_required', 'authorized_users', 'password'), 
  'classes': ('collapse', 'collapse-closed')}),) + \
    EntryAdmin.fieldsets[3:]
  filter_horizontal = EntryAdmin.filter_horizontal + ('authorized_users',)

  def queryset(self, request):
        """Make special filtering by user permissions"""
        if not request.user.has_perm('zinnia.can_view_all'):
            queryset = request.user.authorizedentry.all() ### changed entries.all() to authorizedentry.all()
        else:
            queryset = super(AuthorizedEntryAdmin, self).queryset(request) ### changed EntryAdmin to AuthorizedEntryAdmin
        return queryset.prefetch_related('categories', 'authors', 'sites')

# Unregister the default EntryAdmin
# then register the EntryCheckAdmin class
#admin.site.unregister(Entry)
#admin.site.register(Entry, EntryCheckAdmin)


#admin.site.register(AuthorizedEntry, EntryAdmin)
