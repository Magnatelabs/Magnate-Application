from django.db import models
from waitinglist.models import WaitingListEntry
from django.utils import timezone
from django import forms

class QuestionList (models.Model):
    waitinglistemail = models.EmailField()
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    created = models.DateTimeField(editable=False)
    sex =  models.CharField(max_length=200)
    dob = models.DateField()
    funding_knowledge = models.CharField(max_length=200)
#    income = models.CharField(max_length=200) need to make this charfield during production
    income = models.PositiveIntegerField(editable=False, default=0)
    funding_preference = models.CharField(max_length=200)
    industry_preference = models.CharField(max_length=200)
    site_rec = models.CharField(max_length=200)

    def __unicode__(self):
        return self.first_name

