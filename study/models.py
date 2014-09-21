from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

from forum.models.action import ActionProxy
from django.utils.translation import ugettext as _
import datetime

class StudyModel(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    entity = models.CharField(max_length=255)
    entity_url = models.CharField(max_length=255)
    description = models.TextField(max_length=750)
    docfile = models.FileField(upload_to='study_uploads/%Y/%m/%d')
    industry = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.entity)

class ProposeCompanyAction(ActionProxy):
    verb=_("proposed")

    def process_data(self, form, docfile):
        entry = StudyModel()
        entry.entity = form.data['entity']
        entry.entity_url = form.data['entity_url']
        entry.description = form.data['description']
        entry.industry = form.data['industry']
        entry.created = datetime.datetime.now()
        entry.docfile = docfile
        entry.user = self.user        
        entry.save()




    def describe(self, viewer=None):
        return _("%(user)s proposed a new startup %(entity)s") % {
            'user': self.hyperlink(self.user.get_profile_url(), self.friendly_username(viewer, self.user)),
            'entity': self.hyperlink(self.study.entity_url, self.study.entity)
        }
