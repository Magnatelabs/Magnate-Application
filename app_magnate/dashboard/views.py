from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

def dashboard_index(request):
    if not request.user.is_authenticated():
        return redirect('/account/login/?next=%s' % request.path)

    return render(request, 'dashboard/dashboard_main.html')

