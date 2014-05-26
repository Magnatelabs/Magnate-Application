from django.db import models
from django.utils import timezone
import datetime

import pdb

class PlatformStatistics (models.Model):
    stat_name = models.CharField(max_length=100)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)   

    def __unicode__(self):
        return self.first_name


def get_stat(stat_name):   # FIXME: make sure works properly when does not exist
    try:
        return PlatformStatistics.objects.get(stat_name=stat_name).value
    except PlatformStatistics.DoesNotExist:
        return None
        
def set_stat(stat_name, value):
    try:
        s = PlatformStatistics.objects.get(stat_name=stat_name)
        s.value=value
        s.timestamp=datetime.datetime.now()
 #       pdb.set_trace()
        s.save()
    except PlatformStatistics.DoesNotExist:
        PlatformStatistics.objects.create(stat_name=stat_name, value=value)
        


