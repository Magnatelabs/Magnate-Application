from django.db import models
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
import datetime

from companyinfo.models import MediaUpdates
from companyinfo.forms import MediaUpdatesForm


def rewards_index(request):
    return render(request, 'rewards/rewards_home.html')


