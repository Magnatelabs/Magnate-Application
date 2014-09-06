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
from django.template import RequestContext, loader, Context
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

#!!!imports to pass fake data!!!
from donations.models import BillingInfo, MagnateFund, PortfolioCompany
from donations.utils import total_donation_amount, all_donations_by_user
from bonus_awards.utils import total_bonus_amount

#imports to recognize django messages
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

#imports for Zinnia content
from django.utils import simplejson
from django.http import HttpResponse

import zinnia
from zinnia.views.archives import EntryIndex
from zinnia.models.entry import Entry


@login_required 
def groups_index(request):
	#for fake data in page
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()

	return render(request, 'groups/groups_all.html', {'funds': funds, 'portfolio': portfolio, })
#    return render(request, 'groups/groups_home.html')


@login_required 
def groups_detail_home(request):
	#for fake data in page
	tda=total_donation_amount(request.user)
	user_has_donation = (tda > 0)
	tba=total_bonus_amount(request.user)
	adu=all_donations_by_user(request.user)
	gt= tda+tba
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()


	return render(request, 'groups/groups_home.html', {'funds': funds, 'portfolio': portfolio, 'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt, 'all_donations_by_user': adu })
#	return render(request, 'groups/groups_detail.html')


@login_required 
def groups_detail_information(request):
	#for fake data in page
	tda=total_donation_amount(request.user)
	user_has_donation = (tda > 0)
	tba=total_bonus_amount(request.user)
	adu=all_donations_by_user(request.user)
	gt= tda+tba
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()


	return render(request, 'groups/groups_info.html', {'funds': funds, 'portfolio': portfolio, 'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt, 'all_donations_by_user': adu })
#	return render(request, 'groups/groups_info.html')

@login_required 
def groups_detail_objective(request):
	#for fake data in page
	tda=total_donation_amount(request.user)
	user_has_donation = (tda > 0)
	tba=total_bonus_amount(request.user)
	adu=all_donations_by_user(request.user)
	gt= tda+tba
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()


	return render(request, 'groups/groups_objective.html', {'funds': funds, 'portfolio': portfolio, 'user_has_donation': user_has_donation, 'total_donation_amount': tda, 'total_bonus_amount': tba, 'grand_total': gt, 'all_donations_by_user': adu })
#	return render(request, 'groups/groups_objective.html')