from django.contrib import admin
from admin_enhancer.admin import EnhancedModelAdminMixin
from rewards.models import Agenda, HangoutAgenda, FundraisingAgenda
from django.db import models
from .widgets import ExtraWidget


import django.forms as forms

class AgendaModelForm(forms.ModelForm):

    extra_data = forms.Field(widget=ExtraWidget)

    def __init__(self, *args, **kwargs):
        super(AgendaModelForm, self).__init__(*args, **kwargs)

        if self.instance.pk is None: # new model
            self.fields['extra_data'].initial = False # indicate that
        else:
            # Take the "extra" field from the model
            extra = self.instance.extra
            if extra is None: # no value
                extra = self.instance.defaultExtra()
            self.fields['extra_data'].initial = extra
        self.fields['extra_data'].required = False

    def save(self, commit=True):
        # this is what the widget returned in value_from_datadict
        extra_data = self.cleaned_data.get('extra_data', None)
        instance = super(AgendaModelForm, self).save(commit=False)
        # Save the data back into the model
        instance.extra = extra_data

        if commit:
            instance.save()
        return super(AgendaModelForm, self).save(commit=commit)

    class Meta:
        model = Agenda

# Using EnhancedModelAdminMixin from admin-enhancer
# this way the admin editing a particular agenda (e.g. hangout) can go
# straight to editing the corresponding Zinnia entry.
class AgendaAdmin(EnhancedModelAdminMixin, admin.ModelAdmin):
    form = AgendaModelForm
    readonly_fields = ( 'user', 'agenda_type',  )

    # Automatically recording the user who created the agenda (e.g. hangout)
    # This user will see the agenda on the dashboard; other won't
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()



# from http://stackoverflow.com/questions/13817525/django-admin-make-all-fields-readonly
from django.contrib.admin.util import flatten_fieldsets
class ReadonlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, extra_context=None):
        return False

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

