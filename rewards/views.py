from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime

from companyinfo.models import MediaUpdates
from companyinfo.forms import MediaUpdatesForm

from zinnia.views.archives import EntryIndex
from zinnia.models.entry import Entry


class RewardsView(EntryIndex):
    def get_template_names(self):
        return ['rewards/rewards_home.html']
    def get_queryset(self): # TODO: unit test that we only show published entries, and only those that have an associated hangout
        return Entry.published.filter(hangout__isnull=False)

def rewards_index(request):
    return RewardsView.as_view()(request, template_name='rewards/rewards_home.html')
#    return render(request, 'rewards/rewards_home.html')


