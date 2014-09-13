from django.contrib import admin
from admin_enhancer.admin import EnhancedModelAdminMixin
from rewards.models import Agenda, HangoutAgenda, FundraisingAgenda
from django.db import models
from .widgets import ExtraWidget


import django.forms as forms

class YourModelForm(forms.ModelForm):

    extra_data = forms.Field(widget=ExtraWidget) #forms.CharField()

    def __init__(self, *args, **kwargs):
        super(YourModelForm, self).__init__(*args, **kwargs)
        # Take the "extra" field from the model
        extra = self.instance.extra
        if extra is None: # new model or somehow no value
            extra = self.instance.defaultExtra()
        self.fields['extra_data'].initial = extra

    def save(self, commit=True):
        # this is what the widget returned in value_from_datadict
        extra_data = self.cleaned_data.get('extra_data', None)
        instance = super(YourModelForm, self).save(commit=False)
        # Save the data back into the model
        instance.extra = extra_data

        if commit:
            instance.save()
        return super(YourModelForm, self).save(commit=commit)

    class Meta:
        model = Agenda

# Using EnhancedModelAdminMixin from admin-enhancer
# this way the admin editing a particular agenda (e.g. hangout) can go
# straight to editing the corresponding Zinnia entry.
class AgendaAdmin(EnhancedModelAdminMixin, admin.ModelAdmin):
    form = YourModelForm
    readonly_fields = ( 'user', 'agenda_type',  )

    # Automatically recording the user who created the agenda (e.g. hangout)
    # This user will see the agenda on the dashboard; other won't
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


class AgendaAdmin2(EnhancedModelAdminMixin, admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user', 'agenda_type', 'date', 'status', 'admin_note', ),
        }),
    )
     
    readonly_fields = ( 'user', 'agenda_type',  )


    formfield_overrides = {
        models.TextField: {'widget': ExtraWidget}
    }

    # edit the "Extra" part
    def formfield_for_dbfield(self, db_field, **kwargs):
        #kwargs['widget']=None

        #if db_field.name == 'extra':
        #    print 'hi'
        #    kwargs['widget'] = ExtraWidget
        return super(AgendaAdmin, self).formfield_for_dbfield(db_field, **kwargs)


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

