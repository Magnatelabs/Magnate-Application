from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

def dashboard_index(request):
    return render(request, 'dashboard/dashboard_main.html')
