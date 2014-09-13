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


  # Detect if there is a section called Privacy. There probably is.
  # Remove it, if it is present, and insert a new Privacy section at the end.
  l = EntryAdmin.fieldsets
  fieldsets = [x for x in l if unicode(x[0]) not in  ['Privacy', 'Templates']] + [(_('Privacy'), {'fields': (
      'login_required', 'authorized_users', 'password'), 
  'classes': ('collapse', 'collapse-closed')}),] 

# This code below stopped working after Zinnia added another section to admin.
#
#  fieldsets = EntryAdmin.fieldsets[:2] + ((_('Privacy'), {'fields': (
#      'login_required', 'authorized_users', 'password'), 
#  'classes': ('collapse', 'collapse-closed')}),) + \
#    EntryAdmin.fieldsets[3:]
  filter_horizontal = EntryAdmin.filter_horizontal + ('authorized_users',)

# Unregister the default EntryAdmin
# then register the EntryCheckAdmin class

admin.site.unregister(Entry)
admin.site.register(Entry, EntryCheckAdmin)
