from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User


class EmailShareModel(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(editable=False)
    share_email_list = models.TextField(max_length=750)
    share_email_content = models.TextField(max_length=750)

