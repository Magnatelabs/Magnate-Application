from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User

class BillingInfo (models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city =  models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    def __unicode__(self):
        return self.first_name

