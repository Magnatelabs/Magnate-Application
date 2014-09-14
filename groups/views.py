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
from zinnia.models import Category

from forum.modules import decorate
from forum.views.commands import AnonymousNotAllowedException
from forum.views.decorators import command, CommandException
from glue_osqa.models import UserCategoryFollowing

from rewards.models import FundraisingAgenda
from zinnia.managers import PUBLISHED
from rewards.models import ACTIVE

@login_required 
def groups_index(request):
	#for fake data in page
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()
	following = set([ucf.category.pk for ucf in request.user.following.all()])
	categories = [(c, c.pk in following) for c in Category.objects.all()]
	return render(request, 'groups/groups_all.html', {'categories': categories, 'following': [], 'funds': funds, 'portfolio': portfolio, })
#    return render(request, 'groups/groups_home.html')


@login_required 
def groups_detail_home(request, id):
	category = get_object_or_404(Category, id=id)
	user = request.user

###	following = set([ucf.category.pk for ucf in request.user.following.all()])
	# this may be an overkill:
	# we are ensuring that the FundraisingAgenda is ACTIVE and
	# also that the Zinnia entry is published.
	fundraising = FundraisingAgenda.objects.filter(entry__categories__pk__in=[category.pk]).filter(entry__status=PUBLISHED).filter(status=ACTIVE).distinct()
	# should I order by -date or by -entry__creation_date?
	fundraising = fundraising.order_by('-date')

	feed = [fa.entry for fa in fundraising]
	current_objective = fundraising[0] if not len(fundraising)==0 else None
	
	#for fake data in page
	tda=total_donation_amount(request.user)
	user_has_donation = (tda > 0)
	tba=total_bonus_amount(request.user)
	adu=all_donations_by_user(request.user)
	gt= tda+tba
	funds = MagnateFund.objects.all()
	portfolio = PortfolioCompany.objects.all()


	return render(request, 'groups/groups_home.html', {
		'category': category, 
		'feed': feed, 
		'current_objective': current_objective, 
		'funds': funds, 
		'portfolio': portfolio, 
		'user_has_donation': user_has_donation, 
		'total_donation_amount': tda, 
		'total_bonus_amount': tba, 
		'grand_total': gt, 
		'all_donations_by_user': adu })
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


@decorate.withfn(command)
def ajax_follow_category(request, id):
    category = get_object_or_404(Category, id=id)
    user = request.user

    if not user.is_authenticated():
        raise AnonymousNotAllowedException(_('follow category'))

    command = request.POST.get('command', '')
    
    if not command in ['follow', 'unfollow']:
    	raise CommandException("Unknown command: %s" % (command))

    to_follow = (command == 'follow')

    # Ignoring to_follow. Just toggle.

    try:
    	rel = user.following.get(category__pk=category.pk)
        rel.delete()    	
    	added = False
    except UserCategoryFollowing.DoesNotExist:
    	UserCategoryFollowing.objects.create(user=user, category=category)
    	added = True
    except UserCategoryFollowing.MultipleObjectsReturned:
    	print 'WARNING. Fixing problem. MultipleObjectsReturned user=%s category=%s' % (user, category)
    	user.following.filter(category__pk=category.pk).delete()
    	added = False

    return {
    'commands': {
    'update_button_text': added and 'Unfollow' or 'Follow',
    }
    }
