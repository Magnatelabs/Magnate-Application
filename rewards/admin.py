from django.contrib import admin
from admin_enhancer.admin import EnhancedModelAdminMixin
from rewards.models import Hangout


# Using EnhancedModelAdminMixin from admin-enhancer
# this way the admin editing a particular hangout can go
# straight to editing the corresponding Zinnia entry.
class HangoutAdmin(EnhancedModelAdminMixin, admin.ModelAdmin):
    readonly_fields = ( 'user',)

    # Automatically recording the user who created the hangout
    # This user will see the hangout on the dashboard; other won't
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Hangout, HangoutAdmin)

