from django.db import models

class Poll(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    email
