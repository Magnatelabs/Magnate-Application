from django.db import models
from django.utils import timezone

from django.utils.translation import ugettext_lazy as _

class MediaUpdates(models.Model):
#    signup_email = models.EmailField()
    signup_email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.name
