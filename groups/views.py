from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.utils import timezone
import datetime
import time
import logging

from django.contrib.auth.models import User
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

#imports to pass fake data 
from donations.models import BillingInfo, MagnateFund, PortfolioCompany
from donations.utils import total_donation_amount
from bonus_awards.utils import total_bonus_amount


@login_required 
def groups_index(request):
	#for fake data in page
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()

	return render(request, 'groups/groups_home.html', {'funds': funds, 'portfolio': portfolio, })
#    return render(request, 'groups/groups_home.html')