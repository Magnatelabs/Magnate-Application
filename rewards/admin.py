from django.contrib import admin
from admin_enhancer.admin import EnhancedModelAdminMixin
from rewards.models import Agenda, HangoutAgenda, FundraisingAgenda


# Using EnhancedModelAdminMixin from admin-enhancer
# this way the admin editing a particular agenda (e.g. hangout) can go
# straight to editing the corresponding Zinnia entry.
class AgendaAdmin(EnhancedModelAdminMixin, admin.ModelAdmin):
    readonly_fields = ( 'user', 'agenda_type', )

    # Automatically recording the user who created the agenda (e.g. hangout)
    # This user will see the agenda on the dashboard; other won't
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


# from http://stackoverflow.com/questions/13817525/django-admin-make-all-fields-readonly
from django.contrib.admin.util import flatten_fieldsets
class ReadonlyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
#        if request.user.is_superuser:
#            return self.readonly_fields

        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

admin.site.register(Agenda, ReadonlyAdmin) # don't mess with this
admin.site.register(HangoutAgenda, AgendaAdmin)
admin.site.register(FundraisingAgenda, AgendaAdmin)

