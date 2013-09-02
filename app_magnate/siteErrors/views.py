from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

def index_404(request):
    return render(request, 'siteErrors/404.html')

def index_500(request):
    return render(request, 'siteErrors/500.html')
