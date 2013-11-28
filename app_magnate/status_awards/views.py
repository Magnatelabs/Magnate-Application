from django.db import models
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.template import RequestContext


def status_index(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'status_awards/status_home.html')


def award_detail(request):
#    if not request.user.is_authenticated():
#        return redirect('/donations/user/?next=%s' % request.path)

    return render(request, 'status_awards/status_award_detail.html')
