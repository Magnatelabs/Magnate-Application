from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User


class StudyModel(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    entity = models.CharField(max_length=255)
    entity_url = models.CharField(max_length=255)
    description = models.TextField(max_length=750)
    docfile = models.FileField(upload_to='study_uploads/%Y/%m/%d')
    industry = models.CharField(max_length=255)

    def __unicode__(self):
        return self.first_name
