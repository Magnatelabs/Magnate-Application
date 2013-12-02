from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin

class EntryCheckAdmin(EntryAdmin):
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

# Unregister the default EntryAdmin
# then register the EntryCheckAdmin class
admin.site.unregister(Entry)
admin.site.register(Entry, EntryCheckAdmin)
