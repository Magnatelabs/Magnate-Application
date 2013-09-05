from django.db import models
from waitinglist.models import WaitingListEntry
from django.utils import timezone
#from django import forms
from django.contrib.auth.models import User

class SpotlightRequest(models.Model):
    user = models.ForeignKey(User)
    company = models.CharField(max_length=200)
    platform = models.CharField(max_length=200)
    request_created = models.DateTimeField(editable=False)
    industry =  models.CharField(max_length=200)
    reason = models.CharField(max_length=200)
    amount = models.CharField(max_length=100)
    deadline = models.DateField()

    def __unicode__(self):
        return self.company
